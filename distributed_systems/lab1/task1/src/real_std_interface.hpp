#include <fcntl.h>
#include<unistd.h>

/*The open() system call opens the file specified by pathname.  If
       the specified file does not exist, it may optionally (if O_CREAT
       is specified in flags) be created by open().

       The return value of open() is a file descriptor, a small,
       nonnegative integer that is an index to an entry in the process's
       table of open file descriptors.
       https://man7.org/linux/man-pages/man2/open.2.html
       */
int open(const char *pathname, mode_t mode);

/*read() attempts to read up to count bytes from file descriptor fd
       into the buffer starting at buf.

       On files that support seeking, the read operation commences at
       the file offset, and the file offset is incremented by the number
       of bytes read.  If the file offset is at or past the end of file,
       no bytes are read, and read() returns zero.*/
ssize_t read(int fd, void* buf, size_t count);

/*write() writes up to count bytes from the buffer starting at buf
       to the file referred to by the file descriptor fd.
*/
ssize_t write(int fd, const void* buf, size_t count);

/*lseek() repositions the file offset of the open file description
       associated with the file descriptor fd to the argument offset
       according to the directive whence as follows:*/
off_t lseek(int fd, off_t offset, int whence);

/*  The chmod() and fchmod() system calls change a file's mode bits.
       (The file mode consists of the file permission bits plus the set-
       user-ID, set-group-ID, and sticky bits.)  These system calls
       differ only in how the file is specified:*/
int chmod(const char *pathname, mode_t mode);

/*unlink() deletes a name from the filesystem.  If that name was
       the last link to a file and no processes have the file open, the
       file is deleted and the space it was using is made available for
       reuse.*/
int unlink(const char *pathname);

/*rename() renames a file, moving it between directories if
       required.  Any other hard links to the file (as created using
       link(2)) are unaffected.  Open file descriptors for oldpath are
       also unaffected.*/
int rename(const char *oldpath, const char *newpath);