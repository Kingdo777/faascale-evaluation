//
// Created by kingdo on 23-9-30.
//

#include <sys/mman.h>
#include <sys/resource.h>
#include <cstdio>
#include <cstring>
#include <csignal>
#include <fcntl.h>
#include <string>
#include <linux/userfaultfd.h>
#include <sys/ioctl.h>
#include <unistd.h>
#include <sys/syscall.h>
#include <err.h>
#include <sys/poll.h>
#include "userpopulatefd.h"

static void *
fault_handler_thread(void *arg);

// 1GB
//#define SIZE (1<<30)
// 3G
#define SIZE (3l*1024*1024*1024)

void print_page_faults(const std::string &msg = "") {
    struct rusage usage{};
    getrusage(RUSAGE_SELF, &usage);
    printf("Major: %ld, Min: %ld\t%s\n", usage.ru_majflt, usage.ru_minflt, msg.c_str());
}

void write(void *addr, size_t len) {
    for (int i = 0; i < len; i += 4096) {
        *((volatile char *) addr + i) = 0;
    }

}

void read(void *addr, size_t len) {
    auto start_time = clock();
    for (int i = 0; i < len; i += 4096) {
        char c = *((char *) addr + i);
    }
    auto end_time = clock();
    printf("Read time: %lf ms\n", static_cast<double >(end_time - start_time) / 1000.0);
}

void spin() {
    // about 10s
    for (long i = 0; i < 3000000000; ++i) {
    }
}

int main() {
    void *addr;
    unsigned long start_time;
//    //################################################ Write-with-pagefault ################################################
//    addr = mmap(nullptr, SIZE, PROT_READ | PROT_WRITE, MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);
//    start_time = clock();
//    write(addr, SIZE);
//    printf("Write-with-pagefault,\t\t write-time-1: %.2lfms", static_cast<double >(clock() - start_time) / 1000.0);
//    start_time = clock();
//    write(addr, SIZE);
//    printf(" write-time: %.2lfms\n", static_cast<double >(clock() - start_time) / 1000.0);
//    munmap(addr, SIZE);
//    //################################################ Write-with-madvise-WILLNEED ################################################
//    addr = mmap(nullptr, SIZE, PROT_READ | PROT_WRITE, MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);
//    start_time = clock();
//    madvise(addr, SIZE, MADV_WILLNEED);
//    printf("Write-with-madvise-WILLNEED,\t madvise-time: %.2lfms", static_cast<double >(clock() - start_time) / 1000.0);
//    start_time = clock();
//    write(addr, SIZE);
//    printf(" write-time: %.2lfms\n", static_cast<double >(clock() - start_time) / 1000.0);
//    munmap(addr, SIZE);
//    //################################################ Write-with-madvise-WILLNEED-pp ################################################
//    addr = mmap(nullptr, SIZE, PROT_READ | PROT_WRITE, MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);
//    start_time = clock();
//    for (int i = 0; i < SIZE; i += 4096) {
//        madvise((char *) addr + i, 4096, MADV_WILLNEED);
//    }
//    printf("Write-with-madvise-WILLNEED-pp,\t madvise-time: %.2lfms",
//           static_cast<double >(clock() - start_time) / 1000.0);
//    start_time = clock();
//    write(addr, SIZE);
//    printf(" write-time: %.2lfms\n", static_cast<double >(clock() - start_time) / 1000.0);
//    munmap(addr, SIZE);
//    //################################################ Write-with-madvise-POP_WRITE ################################################
//    addr = mmap(nullptr, SIZE, PROT_READ | PROT_WRITE, MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);
//    start_time = clock();
//    madvise(addr, SIZE, MADV_POPULATE_WRITE);
//    printf("Write-with-madvise-POP_WRITE,\t madvise-time: %.2lfms",
//           static_cast<double >(clock() - start_time) / 1000.0);
//    start_time = clock();
//    write(addr, SIZE);
//    printf(" write-time: %.2lfms\n", static_cast<double >(clock() - start_time) / 1000.0);
//    munmap(addr, SIZE);
//    //################################################ Write-with-madvise-POP_WRITE-pp ################################################
//    addr = mmap(nullptr, SIZE, PROT_READ | PROT_WRITE, MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);
//    start_time = clock();
//    for (int i = 0; i < SIZE; i += 4096) {
//        madvise((char *) addr + i, 4096, MADV_POPULATE_WRITE);
//    }
//    printf("Write-with-madvise-per-page,\t madvise-time: %.2lfms", static_cast<double >(clock() - start_time) / 1000.0);
//    start_time = clock();
//    write(addr, SIZE);
//    printf(" write-time: %.2lfms\n", static_cast<double >(clock() - start_time) / 1000.0);
//    munmap(addr, SIZE);
//
//    //################################################# Write-with-userfaultfd ################################################
//    addr = mmap(nullptr, SIZE, PROT_READ | PROT_WRITE, MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);
//
//    long uffd;    /* userfaultfd file descriptor */
//    struct uffdio_api uffdio_api{};
//    struct uffdio_register uffdio_register{};
//    struct uffdio_copy uffdio_copy{};
//
//    uffd = syscall(SYS_userfaultfd, O_CLOEXEC | O_NONBLOCK);
//
//    uffdio_api.api = UFFD_API;
//    uffdio_api.features = 0;
//    ioctl(uffd, UFFDIO_API, &uffdio_api);
//
//    uffdio_register.range.start = (unsigned long) addr;
//    uffdio_register.range.len = SIZE;
//    uffdio_register.mode = UFFDIO_REGISTER_MODE_MISSING;
//    ioctl(uffd, UFFDIO_REGISTER, &uffdio_register);
//
//    auto addr_ = mmap(nullptr, SIZE, PROT_READ | PROT_WRITE, MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);
//    memset(addr_, 'K', SIZE);
//
//    start_time = clock();
//    uffdio_copy.src = (unsigned long) addr_;
//    uffdio_copy.dst = (unsigned long) addr;
//    uffdio_copy.len = SIZE;
//    uffdio_copy.mode = 0;
//    uffdio_copy.copy = 0;
//    ioctl(uffd, UFFDIO_COPY, &uffdio_copy);
//    printf("Write-with-userfaultfd,\t\t copy-time: %.2lfms",
//           static_cast<double >(clock() - start_time) / 1000.0);
//    start_time = clock();
//    write(addr, SIZE);
//    printf(" write-time: %.2lfms\n", static_cast<double >(clock() - start_time) / 1000.0);
//    munmap(addr, SIZE);
//    munmap(addr_, SIZE);

//    //################################################# Write-with-userfaultfd ################################################
    addr = mmap(nullptr, SIZE, PROT_READ | PROT_WRITE, MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);
    void *addr_ = mmap(nullptr, SIZE, PROT_READ | PROT_WRITE, MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);
    memset(addr_, 'K', SIZE);

    int fd = open("/dev/userpopulatefd", O_RDWR);
    if (fd == -1) {
        perror("Failed to open the device file");
        return 1;
    }
    struct upfdio_graft upfdio_graft = {
            .src= (unsigned long) addr_,
            .dst = (unsigned long) addr,
            .len = SIZE,
    };

    start_time = clock();
    if (ioctl(fd, UPFDIO_GRAFT, &upfdio_graft) == -1) {
        perror("Failed to perform ioctl");
        close(fd);
        return 1;
    }
    printf("Write-with-userpopulatefd,\t\t copy-time: %.2lfms",
           static_cast<double >(clock() - start_time) / 1000.0);
    start_time = clock();
    write(addr, SIZE);
    printf(" write-time: %.2lfms\n", static_cast<double >(clock() - start_time) / 1000.0);
    munmap(addr, SIZE);
    munmap(addr_, SIZE);




//    addr = mmap(nullptr, SIZE, PROT_READ | PROT_WRITE, MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);
//    start_time = clock();
//    write(addr, SIZE);
//    printf("Write-First,\t write-time-1: %.2lfms\n", static_cast<double >(clock() - start_time) / 1000.0);
//
//    start_time = clock();
//    write(addr, SIZE);
//    printf("Write-Second,\t write-time-1: %.2lfms\n", static_cast<double >(clock() - start_time) / 1000.0);
//
//    madvise(addr, SIZE, MADV_DONTNEED);
//    start_time = clock();
//    write(addr, SIZE);
//    printf("Write-DONTNEED,\t write-time-1: %.2lfms\n",
//           static_cast<double >(clock() - start_time) / 1000.0);
//
//    madvise(addr, SIZE, MADV_REMOVE);
//    start_time = clock();
//    write(addr, SIZE);
//    printf("Write-REMOVE,\t write-time-1: %.2lfms\n",
//           static_cast<double >(clock() - start_time) / 1000.0);
//    munmap(addr, SIZE);

    return 0;
}


static void *
fault_handler_thread(void *arg) {
    int nready;
    long uffd;   /* userfaultfd file descriptor */
    ssize_t nread;
    struct pollfd pollfd{};
    struct uffdio_continue uffdio_continue{};
    static struct uffd_msg msg;  /* Data read from userfaultfd */

    auto fd_ = open("/dev/shm/my_shmem_4KB", O_RDWR);
    auto addr_ = mmap(nullptr, SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd_, 0);
//    auto addr_ = mmap(nullptr, SIZE, PROT_READ | PROT_WRITE, MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);
    if (addr_ == MAP_FAILED)
        err(EXIT_FAILURE, "mmap");
    memset(addr_, 'K', SIZE);

    uffd = (long) arg;

    for (;;) {

        pollfd.fd = uffd;
        pollfd.events = POLLIN;
        nready = poll(&pollfd, 1, -1);
        if (nready == -1)
            err(EXIT_FAILURE, "poll");

        nread = read(uffd, &msg, sizeof(msg));
        if (nread == 0) {
            printf("EOF on userfaultfd!\n");
            exit(EXIT_FAILURE);
        }


        if (nread == -1)
            err(EXIT_FAILURE, "read");


        if (msg.event != UFFD_EVENT_PAGEFAULT) {
            fprintf(stderr, "Unexpected event on userfaultfd\n");
            exit(EXIT_FAILURE);
        }

        if (msg.arg.pagefault.flags != UFFD_PAGEFAULT_FLAG_MINOR) {
            fprintf(stderr, "Unexpected flags on userfaultfd\n");
            exit(EXIT_FAILURE);
        }


        uffdio_continue.range.start = (unsigned long) addr_;
        uffdio_continue.range.len = SIZE;
        uffdio_continue.mode = 0;
        if (ioctl(uffd, UFFDIO_CONTINUE, &uffdio_continue) == -1)
            err(EXIT_FAILURE, "ioctl-UFFDIO_CONTINUE");
    }

    munmap(addr_, SIZE);
}
