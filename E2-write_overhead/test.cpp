#include <sys/mman.h>
#include <ctime>
#include <cstdio>
#include <string>
#include <fstream>
#include <iostream>
#include <unistd.h>

#define MB   (1024L * 1024)
#define GB   (1024L * 1024 * 1024)

unsigned long SIZE = 0;

bool enterCgroup() {
    std::string cgroupPath = "/sys/fs/cgroup/memory/test";
    std::string pid = std::to_string(getpid());

    std::ofstream cgroupProcsFile(cgroupPath + "/cgroup.procs");
    if (!cgroupProcsFile.is_open()) {
        std::cerr << "Failed to open cgroup.procs file in " << cgroupPath << std::endl;
        return false;
    }

    cgroupProcsFile << pid;
    cgroupProcsFile.close();

    return true;
}

long write_overhead() {
    char *p = static_cast<char *>(mmap(nullptr, SIZE, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS,
                                       -1, 0));
    if (p == MAP_FAILED) {
        perror("mmap");
        return -1;
    }

    long start = clock();
    for (long i = 0; i < SIZE; i += 4096) {
        *(volatile char *) (p + i) = 0;
    }
    long end = clock();
    printf("Write overhead: %.2lf ms\n", static_cast<double >(end - start) / CLOCKS_PER_SEC * 1000);
    munmap(p, SIZE);
    return end - start;
}

int main(int argc, char **argv) {
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " [512,1,2,3]" << std::endl;
        return -1;
    }

    long size = strtol(argv[1], nullptr, 10);
    switch (size) {
        case 512:
            SIZE = 512 * MB;
            break;
        case 1:
        case 2:
        case 3:
            SIZE = size * GB;
            break;
        default:
            std::cerr << "Invalid size" << std::endl;
            return -1;
    }

    if (enterCgroup())
        write_overhead();
    else
        std::cerr << "Failed to enter cgroup" << std::endl;

    return 0;
}