#ifndef S21_STRING_H
#define S21_STRING_H
#include <stdio.h>
#include <ctype.h>
#include <locale.h>
#include <math.h>
#include <stdarg.h>
#include <stdlib.h>
#include <wchar.h>
typedef unsigned long long s21_size_t;
#define S21_NULL (void *)0

typedef struct var_parameters {
  int align_minus;
  int show_sign;
  int space_for_pos;
  int hash_zero;
  int direct_zero;
  int width;
  int star_width;
  int star_precision;
  int precision_zero;
  int dot_check;
  int precision_num;
  int len_h;
  int len_l;
  int len_double;
} params;

typedef struct {
  int form;
  int supr;
  int width;
  int length;
  long int n;
  char buff;
  int eof;
  int err;
} flags;

/*************** PART1 ****************/

void *s21_memchr(const void *str, int c, s21_size_t n);//Выполняет поиск первого вхождения символа c (беззнаковый тип) в первых n байтах строки, на которую указывает аргумент str.
int s21_memcmp(const void *str1, const void *str2, s21_size_t n);//	Сравнивает первые n байтов str1 и str2.
void *s21_memcpy(void *dest, const void *src, s21_size_t n);// Копирует n символов из src в dest.
void *s21_memmove(void *dest, const void *src, s21_size_t n);// Еще одна функция для копирования n символов из src в dest.
void *s21_memset(void *str, int c, s21_size_t n);// Копирует символ c (беззнаковый тип) в первые n символов строки, на которую указывает аргумент str.
char *s21_strcat(char *dest, const char *src);// Добавляет строку, на которую указывает src, в конец строки, на которую указывает dest.
char *s21_strncat(char *dest, const char *src, s21_size_t n);// Добавляет строку, на которую указывает src, в конец строки, на которую указывает dest, длиной до n символов.
char *s21_strchr(const char *str, int c);// Выполняет поиск первого вхождения символа c (беззнаковый тип) в строке, на которую указывает аргумент str.
int s21_strcmp(const char *str1, const char *str2);// Сравнивает строку, на которую указывает str1, со строкой, на которую указывает str2.
int s21_strncmp(const char *str1, const char *str2, s21_size_t n);// Сравнивает не более первых n байтов str1 и str2.
char *s21_strcpy(char *dest, const char *src);// Копирует строку, на которую указывает src, в dest.
char *s21_strncpy(char *dest, const char *src, s21_size_t n);// Копирует до n символов из строки, на которую указывает src, в dest.
s21_size_t s21_strcspn(const char *str1, const char *str2);// Вычисляет длину начального сегмента str1, который полностью состоит из символов, не входящих в str2.
char *s21_strerror(int errnum);// Выполняет поиск во внутреннем массиве номера strcspn errnum и возвращает указатель на строку с сообщением об ошибке. Нужно объявить макросы, содержащие массивы сообщений об ошибке для операционных систем mac и linux. Описания ошибок есть в оригинальной библиотеке. Проверка текущей ОС осуществляется с помощью директив.
s21_size_t s21_strlen(const char *str);// Вычисляет длину строки str, не включая завершающий нулевой символ.
char *s21_strpbrk(const char *str1, const char *str2);// Находит первый символ в строке str1, который соответствует любому символу, указанному в str2.
char *s21_strrchr(const char *str, int c);// Выполняет поиск последнего вхождения символа c (беззнаковый тип) в строке, на которую указывает аргумент str.
s21_size_t s21_strspn(const char *str1, const char *str2);// Вычисляет длину начального сегмента str1, который полностью состоит из символов str2.
char *s21_strstr(const char *haystack, const char *needle);// Находит первое вхождение всей строки needle (не включая завершающий нулевой символ), которая появляется в строке haystack.
char *s21_strtok(char *str, const char *delim);// Разбивает строку str на ряд токенов, разделенных delim.

/*************** PART2-3 ****************/

int s21_sprintf(char *s, const char *format, ...);

void process_string(va_list ap, params *variable, char *s, int *top);
void process_x(va_list ap, params *variable, long unsigned int v_x, char *array,
               int *top, const char *format);
void process_g(va_list ap, params *variable, long double v_e, char *array,
               int *top, const char *format_pointer);
void process_float(va_list ap, params *variable, long double v_f, char *array,
                   int *top);
void process_exp(va_list ap, params *variable, long double v_e, char *array,
                 int *top, const char *format_pointer);
void process_char(va_list ap, params *variable, char *array, int *top);
void process_int(va_list ap, params *variable, char *array, int *top,
                 const char *gen_pointer);
void process_oct(va_list ap, params *variable, char *array, int *top);
void process_p(va_list ap, params *variable, int *v_p, char *array, int *top);
void write_into_main_buf(const char *temp, char *main_buf, int *top, int count,
                         int flag, int hex_flag, int sign);
void align_left(char *main_buf, int *top, int len, int fill, params *variable,
                const char *temp);
int add_zero(char **temp, char *main_buf, int *top, int len, params *variable,
             int *shift);
void add_space(const char *temp, char *main_buf, int *top, int len,
               params *variable);
int parse_params(const char *str_pointer, params *variable, int *shift);
void init_struct(params *res);
char *s21_itoa(long int num);
char *oct_to_string(long int num, params *variable);
void delete_zero(char *g_string, int *top);
char *hex_to_string(unsigned long int num, int upper_flag, int pointer_flag,
                    int nil_flag);
char *float_to_string(long double num, int g_flag, params *variable);
char *exp_to_string(long double v_e, const char *exp_letter, int g_flag,
                    params *variable);
int check_fraction(int *top, params *variable, long double num);
int check_precision(params *variable, int expo);
int add_precision_zero(char **temp, char *main_buf, int *top, params *variable,
                       int flag_x, int *shift);
void add_space_precision_zero(char *temp, char *main_buf, int *top,
                              params *variable);
int find_exp(long double num);
void long_char_helper(wchar_t *long_str, params *variable, char *s, int *top);
void null_helper(params *variable, char *s, int *top);
void normal_string_helper(char *simple_str, params *variable, char *s,
                          int *top);

/*************** PART4 ****************/

int s21_sscanf(const char *str, const char *format, ...);

int caseInt(va_list args, flags *fl, char **strc, int sys);
int caseUns(va_list args, flags *fl, char **strc, int sys);
int caseFlo(va_list args, flags *fl, char **strc);
int casePtr(va_list args, flags *fl, char **strc);
int caseCha(va_list args, flags *fl, char **strc);
int caseStr(va_list args, flags *fl, char **strc);
void spaceTrim(char **strc, flags *fl);
void casePer(char **strc, flags *fl, const char *format);
int flagsInv(char **strc, flags *fl, const char *format);
void caseN(va_list args, flags *fl);
void caseNonFormat(char **strc, flags *fl, const char *format);
int checkBreak(va_list args, flags *fl, char **strc, const char *format);
int switchFormat(va_list args, flags *fl, char **strc, const char *format);
void numericBuff(char **strc, flags *fl);
long s21_strtol(char *str, char **strend, int sys);
unsigned long s21_strtoul(char *str, char **strend, int sys);
long double s21_strtold(char *str, char **strend);
float s21_strtof(char *str, char **strend);
double s21_strtod(char *str, char **strend);

/*************** PART5 ****************/
void *s21_trim(const char *src, const char *trim_chars);
void *s21_insert(const char *src, const char *str, s21_size_t start_index);
void *s21_to_lower(const char *str);
void *s21_to_upper(const char *str);





// for strerror

#if defined (__APPLE__)
#define err_min 0
#define err_max 107
static char *ErrorsNUM[] = {
        "Undefined error: 0",
        "Operation not permitted",
        "No such file or directory",
        "No such process",
        "Interrupted system call",
        "Input/output error",
        "Device not configured",
        "Argument list too long",
        "Exec format error",
        "Bad file descriptor",
        "No child processes",
        "Resource deadlock avoided",
        "Cannot allocate memory",
        "Permission denied",
        "Bad address",
        "Block device required",
        "Resource busy",
        "File exists",
        "Cross-device link",
        "Operation not supported by device",
        "Not a directory",
        "Is a directory",
        "Invalid argument",
        "Too many open files in system",
        "Too many open files",
        "Inappropriate ioctl for device",
        "Text file busy",
        "File too large",
        "No space left on device",
        "Illegal seek",
        "Read-only file system",
        "Too many links",
        "Broken pipe",
        "Numerical argument out of domain",
        "Result too large",
        "Resource temporarily unavailable",
        "Operation now in progress",
        "Operation already in progress",
        "Socket operation on non-socket",
        "Destination address required",
        "Message too long",
        "Protocol wrong type for socket",
        "Protocol not available",
        "Protocol not supported",
        "Socket type not supported",
        "Operation not supported",
        "Protocol family not supported",
        "Address family not supported by protocol family",
        "Address already in use",
        "Cannot assign requested address",
        "Network is down",
        "Network is unreachable",
        "Network dropped connection on reset",
        "Software caused connection abort",
        "Connection reset by peer",
        "No buffer space available",
        "Socket is already connected",
        "Socket is not connected",
        "Cannot send after socket shutdown",
        "Too many references: Cannot splice",
        "Operation timed out",
        "Connection refused",
        "Too many levels of symbolic links",
        "File name too long",
        "Host is down", "No route to host",
        "Directory not empty",
        "Too many processes",
        "Too many users",
        "Disc quota exceeded",
        "Stale NFS file handle",
        "Too many levels of remote in path",
        "RPC struct is bad",
        "RPC version wrong",
        "RPC prog. not avail",
        "Program version wrong",
        "Bad procedure for program",
        "No locks available",
        "Function not implemented",
        "Inappropriate file type or format",
        "Authentication error",
        "Need authenticator",
        "Device power is off",
        "Device error",
        "Value too large to be stored in data type",
        "Bad executable (or shared library)",
        "Bad CPU type in executable",
        "Shared library version mismatch",
        "Malformed Mach-o file",
        "Operation canceled",
        "Identifier removed",
        "No message of desired type",
        "Illegal byte sequence",
        "Attribute not found",
        "Bad message",
        "EMULTIHOP (Reserved)",
        "No message available on STREAM",
        "ENOLINK (Reserved)",
        "No STREAM resources",
        "Not a STREAM",
        "Protocol error",
        "STREAM ioctl timeout",
        "Operation not supported on socket",
        "Policy not found",
        "State not recoverable",
        "Previous owner died",
        "Interface output queue is full"
};

#elif defined (__linux_)
#define err_min 0
#define err_max 132
static char *ErrorsNUM[] = {
        "Success",
        "Operation not permitted",
        "No such file or directory",
        "No such process",
        "Interrupted system call",
        "Input/output error",
        "No such device or address",
        "Argument list too long",
        "Exec format error",
        "Bad file descriptor",
        "No child processes",
        "Resource temporarily unavailable",
        "Cannot allocate memory",
        "Permission denied",
        "Bad address",
        "Block device required",
        "Device or resource busy",
        "File exists",
        "Invalid cross-device link",
        "No such device",
        "Not a directory",
        "Is a directory",
        "Invalid argument",
        "Too many open files in system",
        "Too many open files",
        "Inappropriate ioctl for device",
        "Text file busy",
        "File too large",
        "No space left on device",
        "Illegal seek",
        "Read-only file system",
        "Too many links",
        "Broken pipe",
        "Numerical argument out of domain",
        "Numerical result out of range",
        "Resource deadlock avoided",
        "File name too long",
        "No locks available",
        "Function not implemented",
        "Directory not empty",
        "Too many levels of symbolic links",
        "Unknown error 41",
        "No message of desired type",
        "Identifier removed",
        "Channel number out of range",
        "Level 2 not synchronized",
        "Level 3 halted",
        "Level 3 reset",
        "Link number out of range",
        "Protocol driver not attached",
        "No CSI structure available",
        "Level 2 halted",
        "Invalid exchange",
        "Invalid request descriptor",
        "Exchange full",
        "No anode",
        "Invalid request code",
        "Invalid slot",
        "Unknown error 58",
        "Bad font file format",
        "Device not a stream",
        "No data available",
        "Timer expired",
        "Out of streams resources",
        "Machine is not on the network",
        "Package not installed",
        "Object is remote",
        "Link has been severed",
        "Advertise error",
        "Srmount error",
        "Communication error on send",
        "Protocol error",
        "Multihop attempted",
        "RFS specific error",
        "Bad message",
        "Value too large for defined data type",
        "Name not unique on network",
        "File descriptor in bad state",
        "Remote address changed",
        "Can not access a needed shared library",
        "Accessing a corrupted shared library",
        ".lib section in a.out corrupted",
        "Attempting to link in too many shared libraries",
        "Cannot exec a shared library directly",
        "Invalid or incomplete multibyte or wide character",
        "Interrupted system call should be restarted", "Streams pipe error",
        "Too many users",
        "Socket operation on non-socket",
        "Destination address required",
        "Message too long",
        "Protocol wrong type for socket",
        "Protocol not available",
        "Protocol not supported",
        "Socket type not supported",
        "Operation not supported",
        "Protocol family not supported",
        "Address family not supported by protocol",
        "Address already in use",
        "Cannot assign requested address",
        "Network is down",
        "Network is unreachable",
        "Network dropped connection on reset",
        "Software caused connection abort",
        "Connection reset by peer",
        "No buffer space available",
        "Transport endpoint is already connected",
        "Transport endpoint is not connected",
        "Cannot send after transport endpoint shutdown",
        "Too many references: cannot splice",
        "Connection timed out",
        "Connection refused",
        "Host is down",
        "No route to host",
        "Operation already in progress",
        "Operation now in progress",
        "Stale file handle",
        "Structure needs cleaning",
        "Not a XENIX named type file",
        "No XENIX semaphores available",
        "Is a named type file",
        "Remote I/O error",
        "Disk quota exceeded",
        "No medium found",
        "Wrong medium type",
        "Operation canceled",
        "Required key not available",
        "Key has expired",
        "Key has been revoked",
        "Key was rejected by service",
        "Owner died",
        "State not recoverable",
        "Operation not possible due to RF-kill",
        "Memory page has hardware error"
};
#endif

#endif