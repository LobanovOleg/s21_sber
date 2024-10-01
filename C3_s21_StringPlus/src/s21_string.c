//Copyright 2022
#include "s21_string.h"

/****** PART1 *****/

void *s21_memchr(const void *str, int c, s21_size_t n) {
//Выполняет поиск первого вхождения символа c (беззнаковый тип)
//в первых n байтах строки, на которую указывает аргумент str.
    
    char *s = (char *) str;// массив проверки
    int check = 0;
    char *result = S21_NULL;//false
    for (s21_size_t i = 0; i < n; i++) {
        if (check == 0) {
            int first = s[i];
            if (first == c) {
              result = (char *)s + i;
              check = 1;
            }
        }
    }
    return check == 0 ? S21_NULL : result;
}
int s21_memcmp(const void *str1, const void *str2, s21_size_t n) {
// сравнение массивов. до N-байтов
// тоже самое что и memchr, 
// но получаем данные уже каждого [i] и сверяем с str2
    const char *s1 = (const char *) str1;
    const char *s2 = (const char *) str2;
    
    int result = 0;
    for (s21_size_t i = 0; i < n ; i++) {
        if (s1[i] != s2[i])
            result = *(s1 + i) - *(s2 + i);
            break;// char - char
    }
    return result;
//  if ( *(char *)str1[*(char)i] != str2[i]) kak??!
//      result = (*(const char *)str1 + i) - (*(const char *)str2 + i);
}
void *s21_memcpy(void *dest, const void *src, s21_size_t n) {
// Копирует n символов из src в dest.
// все аналогично предыдущих functions, только тут str[i] == str2[i]

    char *d = (char *) dest;
    char *s = (char *) src;
    if (dest != S21_NULL && src != S21_NULL) {
      for (s21_size_t i = 0; i < n; i++) {
        d[i] = s[i];
      }
    }
    return dest;
}
s21_size_t s21_strlen(const char *str) {
    return (*str) ? s21_strlen(++str) + 1 : 0;
}
void *s21_memset(void *str, int c, s21_size_t n) {
  char *b = str;
  for (; n > 0; n--) {
    *(b++) = c;
  }
  return str;
}
char *s21_strcat(char *dest, const char *src) {
  int len = 0;
  for (; *(dest + len); len++)
    ;
  int i = 0;
  for (; *(src + i) != '\0'; i++) {
    *(dest + len + i) = *(src + i);
  }
  *(dest + len + i) = '\0';
  return dest;
}
char *s21_strncat(char *dest, const char *src, s21_size_t n) {
 int len = 0;
  for (; *(dest + len); len++)
    ;
  int i = 0;
  for (; *(src + i) != '\0' && i < (int)n; i++) {
    *(dest + len + i) = *(src + i);
  }
  *(dest + len + i) = '\0';
  return dest;
}
char *s21_strchr(const char *str, int c) {
  char *res = NULL;
  int len = 0;
  for (; *(str + len); len++)
    ;
  for (int i = 0; i < len; i++) {
    if (*(str + i) == c) {
      res = (char *)str + i;
      i = len;
    }
  }
  return res;

}
int s21_strcmp(const char *str1, const char *str2) {
    int res = 0;

    if (str1 && str2) {
        int i = 0;

        while (str1[i] && str1[i] == str2[i]) {
            i++;
        }
        res = str1[i] - str2[i];
    }

    return res;

}
int s21_strncmp(const char *str1, const char *str2, s21_size_t n) {
    int res = 0;

    if (str1 && str2 && n > 0) {
        for (s21_size_t i = 0; i < n; i++) {
            if (str1[i] == '\0' || str1[i] != str2[i]) {
                res = str1[i] - str2[i];
                break;
            }
        }
    }
    return res;
}
char *s21_strcpy(char *dest, const char *src) {
    for (int i = 0; src[i]; i++) {
        dest[i] = src[i];
    }

    dest[s21_strlen(src)] = '\0';

    return dest;

}
char *s21_strncpy(char *dest, const char *src, s21_size_t n) {
    s21_memset(dest, '\0', n);

    for (s21_size_t i = 0; i < n && src[i]; i++) {
        dest[i] = src[i];
    }

    return dest;

}
s21_size_t s21_strcspn(const char *str1, const char *str2) {
// Вычисляет длину начального сегмента str1,
// который полностью состоит из символов, не входящих в str2.
    s21_size_t s1 = s21_strlen(str1);
    s21_size_t s2 = s21_strlen(str2);
    s21_size_t i = 0;
    s21_size_t count = 0;
    int flag = 0;
    for (; i < s1; i++) {//1-argv
        if (flag)
            break;
        for (s21_size_t j = 0;j < s2; j++) {//2-argv
            if (str1[i] == str2[j]) {
                count = i;
                flag++;
                break;
            }
        }
    }
    if (!flag)
        count = i;
    return count;
}
char *s21_strpbrk(const char *str1, const char *str2) {
// Находит первый символ в строке str1,
// который соответствует любому символу, указанному в str2.
    int flag = 0;
    char *result = S21_NULL;

    for (int i = 0; str1[i] != '\0' && flag == 0; i++) {
        for (int j = 0; str2[j] != '\0'; j++) {
            if (str1[i] == str2[j]) {
                ++flag;
                result = (char *) str1 + i;//битовая ячейка
            }
        }
    }
    return result;
}
void *s21_memmove(void *dest, const void *src, s21_size_t n) {
// Еще одна функция для копирования n символов из src в dest.
// src[n-байт->] -> dest
    unsigned char *d = (unsigned char *)dest;
    unsigned char *s = (unsigned char *)src;

    if (dest == src || !n)
        return (dest);
    if (src < dest && dest - src < (int)n) {
        for (int i = n - 1; i >= 0; i--)
            d[i] = s[i];
        return dest;
    }
    else {
        for (s21_size_t i = 0; i < n; i++)
            d[i] = s[i];
        return dest;
    }
}
char *s21_strstr(const char *haystack, const char *needle) {
// Находит первое вхождение всей строки needle
// (не включая завершающий нулевой символ), которая появляется в строке haystack.
    char *h_temp, *n_temp; //todo:REMOVE

    if (!*needle)
        return ((char *)haystack);
    while (*haystack) {
        if (*haystack == *needle) {
            h_temp = (char *)haystack; //todo: заменить на strcmp
            n_temp = (char *)needle;
            while (*h_temp++ == *n_temp++) {
                if (!*n_temp) {
                    return (char *)haystack;
                }
            }
        }
        haystack++;
    }
    return S21_NULL;
}
char *s21_strrchr(const char *str, int c) {
    char *ch = S21_NULL;
    size_t a;
    for (a = s21_strlen(str); a > 0; a--) {
        if (str[a] == c) {
            ch = (char*)str + a;
            break;
        } else {
            ch = 0;
        }
    }
    return ch;


}
s21_size_t s21_strspn(const char *str1, const char *str2) {
    s21_size_t a, b;
    for (a = 0; str1[a] != '\0'; a++) {
        for (b = 0; str2[b] != str1[a]; b++) {
            if (str2[b] == '\0') {
                return a;
            }
        }
    }
    return a;

}
char *s21_strtok(char *str, const char *delim) {
    static char *buffer;
    char *token = NULL;

    if (str) {
        buffer = str;
        while (*buffer && s21_strchr(delim, *buffer)) {
            *buffer++ = '\0';
        }
    }
    if (buffer && *buffer) {
        str = buffer;
        while (*buffer && !s21_strchr(delim, *buffer)) {
            ++buffer;
        }
        while (*buffer && s21_strchr(delim, *buffer)) {
            *buffer++ = '\0';
        }
        token = str;
    }
    return token;

}
char *s21_strerror(int errnum) {
    char *output = (char *)calloc(50, sizeof(char));
    if (errnum > err_min && errnum < err_max) {
        s21_sprintf(output, "%s", ErrorsNUM[errnum]);
    } else {
        s21_sprintf(output, "Unknown error");
    }
    output = (char *)realloc(output, s21_strlen(output));
    return output;
}

/****** PART2-3 *****/

#define TOKENS "cdieEfgGosuxXpn"
char conflicting_char = '.';


int s21_sprintf(char *s, const char *format, ...) {
  int top_buffer = 0;
  const char *gen_pointer = S21_NULL;
  int stop_flag = 0;
  long double v_e = 0;
  long double v_f = 0;
  int *v_p = S21_NULL;
  long unsigned int v_x = 0;
  params variable;

  va_list ap;
  va_start(ap, format);
  setlocale(LC_ALL, "");
  setlocale(LC_NUMERIC, "en_US.UTF-8");
  for (gen_pointer = format; *gen_pointer; gen_pointer++) {
    int shift;
    if ((*gen_pointer) != '%') {
      s[top_buffer] = *gen_pointer;
      top_buffer++;
      continue;
    } else {
      shift = 0;
      init_struct(&variable);
      stop_flag = parse_params(gen_pointer, &variable, &shift);
    }
    if (!stop_flag) {
      gen_pointer += shift;
      if (s21_strchr("diu", (int)(*gen_pointer))) {
        process_int(ap, &variable, s, &top_buffer, gen_pointer);
      } else if (*gen_pointer == 'c') {
        process_char(ap, &variable, s, &top_buffer);
      } else if (*gen_pointer == 'E' || *gen_pointer == 'e') {
        process_exp(ap, &variable, v_e, s, &top_buffer, gen_pointer);
      } else if (*gen_pointer == 'f') {
        process_float(ap, &variable, v_f, s, &top_buffer);
      } else if (*gen_pointer == 'G' || *gen_pointer == 'g') {
        process_g(ap, &variable, v_e, s, &top_buffer, gen_pointer);
      } else if (*gen_pointer == 'o') {
        process_oct(ap, &variable, s, &top_buffer);
      } else if (*gen_pointer == 's') {
        process_string(ap, &variable, s, &top_buffer);
      } else if (*gen_pointer == 'x' || *gen_pointer == 'X') {
        process_x(ap, &variable, v_x, s, &top_buffer, gen_pointer);
      } else if (*gen_pointer == 'p') {
        variable.hash_zero = 1;
        process_p(ap, &variable, v_p, s, &top_buffer);
      } else if (*gen_pointer == 'n') {
        int *bytes_num = S21_NULL;
        bytes_num = va_arg(ap, int *);
        *bytes_num = top_buffer;
      } else {
        s[top_buffer] = *gen_pointer;
        top_buffer++;
      }
    }
  }
  s[top_buffer] = '\0';
  va_end(ap);
  return s21_strlen(s);
}
void process_p(va_list ap, params *variable, int *v_p, char *array, int *top) {
  int zero_flag = 0;
  if (variable->star_width == 1) {
    variable->width = va_arg(ap, int);
  }
  v_p = va_arg(ap, int *);
  int nil_flag = 0;
  long long int convert = 0;
  if (v_p != S21_NULL) {
    convert = (long long int)v_p;
  } else {
    nil_flag = 1;
  }
  char *temp = hex_to_string(convert, 0, variable->hash_zero, nil_flag);
  if (variable->width > 0 && variable->align_minus == 0) {
    add_space(temp, array, top, (int)s21_strlen(temp), variable);
  }
  write_into_main_buf(temp, array, top, (int)s21_strlen(temp), zero_flag, 0, 0);
  if (variable->align_minus) {
    align_left(array, top, (int)s21_strlen(temp), variable->width, variable,
               temp);
  }
  free(temp);
}
void process_oct(va_list ap, params *variable, char *array, int *top) {
  int zero_flag = 0;
  long int v_int;
  if (variable->star_width == 1) {
    variable->width = va_arg(ap, int);
  }
  if (variable->star_precision) {
    variable->precision_num = va_arg(ap, int);
  }
  if (variable->precision_num == -1) variable->precision_num = 0;
  if (variable->len_h == 1) {
    v_int = va_arg(ap, int);
  } else if (variable->len_l == 1) {
    v_int = va_arg(ap, long int);
  } else {
    v_int = va_arg(ap, int);
  }
  v_int = (long int)v_int;
  if (variable->precision_num > 0) {
    char *temp_ar = oct_to_string(v_int, variable);
    int size_helper = (variable->hash_zero > 0) ? (s21_strlen(temp_ar) - 1)
                                                : s21_strlen(temp_ar);
    variable->precision_zero = (variable->precision_num - size_helper > 0)
                                   ? (variable->precision_num - size_helper)
                                   : 0;
    free(temp_ar);
  }
  int temp_shift = 0;
  char *temp = oct_to_string(v_int, variable);
  if (variable->precision_zero) {
    if (variable->width > 0 && variable->align_minus == 0) {
      add_space_precision_zero(temp, array, top, variable);
    }
    zero_flag = add_precision_zero(&temp, array, top, variable, 0, &temp_shift);
  } else if (variable->direct_zero) {
    zero_flag = add_zero(&temp, array, top, (int)s21_strlen(temp), variable,
                         &temp_shift);
  } else if (variable->width > 0 && variable->align_minus == 0) {
    add_space(temp, array, top, (int)s21_strlen(temp), variable);
  }
  write_into_main_buf(temp, array, top, (int)s21_strlen(temp), zero_flag, 0, 0);
  if (variable->align_minus) {
    align_left(array, top, (int)s21_strlen(temp), variable->width, variable,
               temp);
  }
  free(temp - temp_shift);
}
char *oct_to_string(long int num, params *variable) {
  char *res = malloc(sizeof(char) * 50);
  if (!res) exit(0);
  char *reverse = malloc(sizeof(char) * 50);
  if (!reverse) {
    free(res);
    exit(0);
  }
  int count = 0;
  int sign = (num >= 0) ? 0 : 1;
  if (num == 0) {
    reverse[count] = '0';
    count++;
  }
  if (!sign) {
    int i = 0;
    long int next = 1;
    long int octanum = 0;
    while (num != 0) {
      octanum = octanum + (num % 8) * next;
      num = num / 8;
      next = next * 10;
    }
    while (octanum > 0) {
      next = octanum % 10;
      reverse[count] = next + '0';
      count++;
      octanum /= 10;
    }
    if (variable->hash_zero) {
      reverse[count] = '0';
      count++;
    }
    for (; i < count; i++) {
      res[i] = reverse[count - i - 1];
    }
    res[i] = '\0';
  } else {
    res[0] = '\0';
  }
  free(reverse);
  return res;
}
void process_string(va_list ap, params *variable, char *s, int *top) {
  char *simple_str = S21_NULL;
  wchar_t *long_str = S21_NULL;
  if (variable->star_width) {
    variable->width = va_arg(ap, int);
  }
  if (variable->star_precision) {
    variable->precision_num = va_arg(ap, int);
  }
  if (variable->len_l == 1) {
    long_str = va_arg(ap, wchar_t *);
    if (!long_str) {
      variable->len_l = 0;
    }
  } else {
    simple_str = va_arg(ap, char *);
  }
  if (variable->len_l == 1) {
    long_char_helper(long_str, variable, s, top);
  } else {
    if (!simple_str) {
      null_helper(variable, s, top);
    } else {
      normal_string_helper(simple_str, variable, s, top);
    }
  }
}
void normal_string_helper(char *simple_str, params *variable, char *s,
                          int *top) {
  char reserve[1000] = {'\0'};
  s21_strcpy(reserve, simple_str);
  int len = (int)s21_strlen(reserve);
  if ((variable->precision_num > 0) && (variable->precision_num < len)) {
    reserve[variable->precision_num] = '\0';
    variable->width -= variable->precision_num;
  } else if (variable->precision_num != 0) {
    variable->width -= len;
  }
  if ((variable->width > 0) && (variable->align_minus == 0)) {
    for (int k = 0; k < variable->width; k++) {
      s[*top] = ' ';
      *top = (*top) + 1;
    }
  }
  if (variable->precision_num != 0) {
    for (int i = 0; i < (int)s21_strlen(reserve); i++) {
      s[*top] = reserve[i];
      *top = (*top) + 1;
    }
  }
  if ((variable->width > 0) && (variable->align_minus == 1)) {
    for (int m = 0; m < variable->width; m++) {
      s[*top] = ' ';
      *top = (*top) + 1;
    }
  }
  s[*top] = '\0';
}
void long_char_helper(wchar_t *long_str, params *variable, char *s, int *top) {
  if (variable->precision_num == -1) variable->precision_num = 0;
  int len = wcslen(long_str);
  int bytes_helper = sizeof(long_str[0]);
  int size_helper = wcstombs(s + (*top), long_str, len * bytes_helper);
  if (variable->precision_num) {
    if (variable->align_minus == 0 && variable->width > size_helper) {
      int space_var = variable->width - variable->precision_num;
      if (space_var > 0) {
        for (int i = 0; i < space_var; i++) {
          s[*top] = ' ';
          *top += 1;
        }
      }
    }
  } else {
    if (variable->align_minus == 0 && variable->width > size_helper) {
      for (int i = 0; i < (variable->width - size_helper); i++) {
        s[*top] = ' ';
        *top += 1;
      }
    }
  }
  if (variable->precision_num) {
    size_helper = (variable->precision_num < size_helper)
                      ? variable->precision_num
                      : size_helper;
  }
  size_helper = wcstombs(s + (*top), long_str, size_helper);
  *top += size_helper;
  if (variable->align_minus == 1 && variable->width > size_helper) {
    if (variable->precision_num > size_helper) {
      int space = variable->width - variable->precision_num;
      if (space > 0) {
        for (int i = 0; i < space; i++) {
          s[*top] = ' ';
          *top += 1;
        }
      }
    } else {
      for (int i = 0; i < (variable->width - size_helper); i++) {
        s[*top] = ' ';
        *top += 1;
      }
    }
  }
}
void null_helper(params *variable, char *s, int *top) {
  char null_str[7] = "(null)";
  int len = (int)s21_strlen(null_str);
  char reserve_buf[10] = {'\0'};
  if ((variable->precision_num > 0) && (variable->precision_num < len)) {
    for (int i = 0; i < variable->precision_num; i++) {
      reserve_buf[i] = null_str[i];
    }
    variable->width -= variable->precision_num;
  } else if (variable->precision_num != 0) {
    for (int j = 0; j < len; j++) {
      reserve_buf[j] = null_str[j];
    }
    variable->width -= len;
  }
  if ((variable->width > 0) && (variable->align_minus == 0)) {
    for (int k = 0; k < variable->width; k++) {
      s[*top] = ' ';
      *top = (*top) + 1;
    }
  }
  for (int l = 0; l < (int)s21_strlen(reserve_buf); l++) {
    s[*top] = reserve_buf[l];
    *top = (*top) + 1;
  }
  if ((variable->width > 0) && (variable->align_minus == 1)) {
    for (int m = 0; m < variable->width; m++) {
      s[*top] = ' ';
      *top = (*top) + 1;
    }
  }
  s[*top] = '\0';
}
void process_x(va_list ap, params *variable, long unsigned int v_x, char *array,
               int *top, const char *format) {
  int zero_flag = 0;
  if (variable->star_width == 1) {
    variable->width = va_arg(ap, int);
  }
  if (variable->star_precision) {
    variable->precision_num = va_arg(ap, int);
  }
  if (variable->precision_num == -1) variable->precision_num = 0;
  if (variable->len_h == 1) {
    v_x = va_arg(ap, int);
  } else if (variable->len_l == 1) {
    v_x = va_arg(ap, long int);
  } else {
    v_x = va_arg(ap, int);
  }
  v_x = (long int)v_x;
  int flag = (*format == 'X') ? 1 : 0;
  if (variable->precision_num > 0) {
    char *temp_ar = hex_to_string(v_x, flag, variable->hash_zero, 0);
    int len_helper = s21_strlen(temp_ar);
    int size_helper = (variable->hash_zero > 0) ? len_helper - 2 : len_helper;
    variable->precision_zero = (variable->precision_num - size_helper > 0)
                                   ? (variable->precision_num - size_helper)
                                   : 0;
    free(temp_ar);
  }
  int temp_shift = 0;
  char *temp = hex_to_string(v_x, flag, variable->hash_zero, 0);
  if (variable->precision_zero) {
    if (variable->width > 0 && variable->align_minus == 0) {
      add_space_precision_zero(temp, array, top, variable);
    }
    zero_flag = add_precision_zero(&temp, array, top, variable, 1, &temp_shift);
  } else if (variable->direct_zero) {
    zero_flag = add_zero(&temp, array, top, (int)s21_strlen(temp), variable,
                         &temp_shift);
  } else if (variable->width > 0 && variable->align_minus == 0) {
    add_space(temp, array, top, (int)s21_strlen(temp), variable);
  }
  int x_flag = (variable->hash_zero > 0) ? 1 : 0;
  write_into_main_buf(temp, array, top, (int)s21_strlen(temp), zero_flag,
                      x_flag, 0);
  if (variable->align_minus) {
    align_left(array, top, (int)s21_strlen(temp), variable->width, variable,
               temp);
  }
  free(temp - temp_shift);
}
void process_g(va_list ap, params *variable, long double v_e, char *array,
               int *top, const char *format_pointer) {
  char *temp = S21_NULL;
  if (variable->star_width) {
    variable->width = va_arg(ap, int);
  }
  if (variable->star_precision) {
    variable->precision_num = va_arg(ap, int);
  }
  if (variable->precision_num == -1) variable->precision_num = 0;
  if (variable->len_double) {
    v_e = va_arg(ap, long double);
  } else {
    v_e = va_arg(ap, double);
  }
  int temp_shift = 0;
  if (v_e >= 0 && variable->show_sign == 1 && variable->width == 0) {
    array[*top] = '+';
    *top += 1;
  }
  if (v_e > 0 && variable->space_for_pos == 1 && variable->width == 0) {
    array[*top] = ' ';
    *top += 1;
  }
  if (v_e == 0) {
    array[*top] = '0';
    *top += 1;
  } else {
    long double pos_v_e = (v_e < 0) ? (v_e * -1) : (v_e);
    int check_exp = find_exp(pos_v_e);
    if (variable->dot_check == 1 && variable->precision_num == 0) {
      variable->precision_num = 1;
    }
    int control = check_precision(variable, check_exp);
    if (control == 1) {
      if (variable->precision_num == 0 && variable->dot_check == 0) {
        variable->precision_num = 5;
      } else if (variable->precision_num > 0) {
        variable->precision_num = variable->precision_num - 1;
      }
      temp = exp_to_string(v_e, format_pointer, 1, variable);
    } else {
      if (variable->precision_num == 0 && variable->dot_check == 0) {
        if (check_exp < 0) {
          check_exp *= -1;
          variable->precision_num = (6 - check_exp);
        } else {
          variable->precision_num = (6 - (check_exp + 1));
        }
      } else if (variable->precision_num == 0 && variable->dot_check == 1) {
        if (check_exp < 0) check_exp *= -1;
        variable->precision_num = check_exp;
      } else if (variable->precision_num > 0) {
        variable->precision_num = (variable->precision_num - (check_exp + 1));
      }
      temp = float_to_string(v_e, 1, variable);
    }
    int zero_flag = 0;
    if (variable->direct_zero) {
      zero_flag = add_zero(&temp, array, top, (int)s21_strlen(temp), variable,
                           &temp_shift);
    } else if (variable->width > 0 && variable->align_minus == 0) {
      add_space(temp, array, top, (int)s21_strlen(temp), variable);
    }
    write_into_main_buf(temp, array, top, (int)s21_strlen(temp), zero_flag, 0,
                        0);
  }
  if (variable->align_minus) {
    align_left(array, top, (int)s21_strlen(temp), variable->width, variable,
               temp);
  }
  array[*top] = '\0';
  free(temp - temp_shift);
}
int find_exp(long double num) {
  int res = 0;
  if (num > 0 && num < 1) {
    while ((long int)num == 0) {
      num = num * 10;
      res++;
    }
    res *= -1;
  } else if (num > 1) {
    while (num != 0) {
      num = (long int)num / 10;
      res++;
    }
    res--;
  }
  return res;
}
void process_float(va_list ap, params *variable, long double v_f, char *array,
                   int *top) {
  int zero_flag = 0;
  if (variable->star_width) {
    variable->width = va_arg(ap, int);
  }
  if (variable->star_precision) {
    variable->precision_num = va_arg(ap, int);
  }
  if (variable->precision_num == -1) variable->precision_num = 0;
  if (variable->len_double) {
    v_f = va_arg(ap, long double);
  } else {
    v_f = va_arg(ap, double);
  }
  if (variable->precision_num == 0 && variable->dot_check == 0) {
    variable->precision_num = 6;
  } else if (variable->precision_num == 0 && variable->dot_check == 1) {
    variable->precision_num = 0;
  }
  if (v_f > 0 && variable->show_sign == 1 && variable->width == 0) {
    array[*top] = '+';
    *top += 1;
  }
  if (v_f >= 0 && variable->space_for_pos == 1 && variable->width == 0) {
    array[*top] = ' ';
    *top += 1;
  }
  int temp_shift = 0;
  char *temp = float_to_string(v_f, 0, variable);
  if (variable->direct_zero == 1) {
    zero_flag = add_zero(&temp, array, top, (int)s21_strlen(temp), variable,
                         &temp_shift);
  } else if (variable->width > 0) {
    add_space(temp, array, top, (int)s21_strlen(temp), variable);
  }
  write_into_main_buf(temp, array, top, (int)s21_strlen(temp), zero_flag, 0, 0);
  if (variable->align_minus) {
    align_left(array, top, (int)s21_strlen(temp), variable->width, variable,
               temp);
  }
  free(temp - temp_shift);
}
void process_exp(va_list ap, params *variable, long double v_e, char *array,
                 int *top, const char *format_pointer) {
  int zero_flag = 0;
  if (variable->star_width) {
    variable->width = va_arg(ap, int);
  }
  if (variable->star_precision) {
    variable->precision_num = va_arg(ap, int);
  }
  if (variable->precision_num == -1) variable->precision_num = 0;
  if (variable->len_double) {
    v_e = va_arg(ap, long double);
  } else {
    v_e = va_arg(ap, double);
  }
  if (variable->dot_check == 1 && variable->precision_num == 0) {
    variable->precision_num = 0;
  } else if (variable->precision_num == 0 && variable->dot_check == 0) {
    variable->precision_num = 6;
  }
  if (v_e > 0 && variable->show_sign == 1 && variable->width == 0) {
    array[*top] = '+';
    *top += 1;
  }
  if (v_e >= 0 && variable->space_for_pos == 1 && variable->width == 0) {
    array[*top] = ' ';
    *top += 1;
  }
  int temp_shift = 0;
  char *temp = exp_to_string(v_e, format_pointer, 0, variable);
  if (variable->direct_zero) {
    zero_flag = add_zero(&temp, array, top, (int)s21_strlen(temp), variable,
                         &temp_shift);
  } else if (variable->width > 0 && variable->align_minus == 0) {
    add_space(temp, array, top, (int)s21_strlen(temp), variable);
  }
  write_into_main_buf(temp, array, top, (int)s21_strlen(temp), zero_flag, 0, 0);
  if (variable->align_minus) {
    align_left(array, top, (int)s21_strlen(temp), variable->width, variable,
               temp);
  }
  free(temp - temp_shift);
}
void process_char(va_list ap, params *variable, char *array, int *top) {
  unsigned char v_char;
  wchar_t long_char;
  if (variable->star_width == 1) {
    variable->width = va_arg(ap, int);
  }
  if (variable->star_precision == 1) {
    variable->precision_num = va_arg(ap, int);
  }
  if (variable->len_l == 1) {
    long_char = va_arg(ap, wchar_t);
  } else {
    v_char = (unsigned char)va_arg(ap, int);
  }
  if (variable->len_l == 1) {
    wchar_t temp[2];
    temp[0] = long_char;
    temp[1] = '\0';
    int size_helper = sizeof(temp[0]);
    int add_size = wcstombs(array + (*top), temp, size_helper);
    if (variable->align_minus == 0 && variable->width > add_size) {
      for (int i = 0; i < (variable->width - add_size); i++) {
        array[*top] = ' ';
        *top += 1;
      }
    }
    add_size = wcstombs(array + (*top), temp, size_helper);
    *top += add_size;
    if (variable->align_minus == 1 && variable->width > add_size) {
      for (int i = 0; i < (variable->width - add_size); i++) {
        array[*top] = ' ';
        *top += 1;
      }
    }
  } else {
    if (variable->align_minus == 0 && variable->width > 1) {
      for (int i = 0; i < (variable->width - 1); i++) {
        array[*top] = ' ';
        *top += 1;
      }
    }
    array[*top] = v_char;
    *top += 1;
    if (variable->align_minus == 1 && variable->width > 1) {
      for (int i = 0; i < (variable->width - 1); i++) {
        array[*top] = ' ';
        *top += 1;
      }
    }
    array[*top] = '\0';
  }
}
void process_int(va_list ap, params *variable, char *array, int *top,
                 const char *gen_pointer) {
  long int v_int = 0;
  if (variable->star_width == 1) {
    variable->width = va_arg(ap, int);
  }
  if (variable->star_precision) {
    variable->precision_num = va_arg(ap, int);
  }
  if (variable->len_h == 1) {
    v_int = ((*gen_pointer) == 'u')
                ? (unsigned short int)va_arg(ap, unsigned int)
                : (short int)va_arg(ap, int);
  } else if (variable->len_l == 1) {
    v_int = ((*gen_pointer) == 'u') ? va_arg(ap, unsigned long int)
                                    : va_arg(ap, long int);
  } else if ((*gen_pointer) == 'u') {
    v_int = va_arg(ap, unsigned int);
  } else {
    v_int = va_arg(ap, int);
  }
  if ((*gen_pointer) == 'u') {
    variable->space_for_pos = 0;
    variable->show_sign = 0;
  }
  char *temp = s21_itoa(v_int);
  int temp_shift = 0;
  int sign = (v_int < 0) ? 1 : 0;
  if (v_int == 0 && variable->precision_num == 0) {
    array[*top] = '\0';
  } else {
    if (variable->precision_num == -1) variable->precision_num = 0;
    if (variable->precision_num > 0) {
      char *temp_ar = s21_itoa(v_int);
      int size_helper =
          (temp_ar[0] == '-') ? s21_strlen(temp_ar + 1) : s21_strlen(temp_ar);
      variable->precision_zero = (variable->precision_num - size_helper > 0)
                                     ? (variable->precision_num - size_helper)
                                     : 0;
      free(temp_ar);
    }
    if (v_int > 0 && variable->show_sign == 1 && variable->width == 0 &&
        variable->precision_zero == 0) {
      array[*top] = '+';
      *top += 1;
    }
    if (v_int >= 0 && variable->space_for_pos == 1 && variable->width == 0) {
      array[*top] = ' ';
      *top += 1;
    }
    int zero_flag = 0;
    if (variable->precision_zero) {
      if (variable->width > 0 && variable->align_minus == 0) {
        add_space_precision_zero(temp, array, top, variable);
      }
      zero_flag =
          add_precision_zero(&temp, array, top, variable, 0, &temp_shift);
      if (temp_shift) sign = 0;
    } else if (variable->direct_zero) {
      zero_flag = add_zero(&temp, array, top, (int)s21_strlen(temp), variable,
                           &temp_shift);
      if (temp_shift) sign = 0;
    } else if (variable->width > 0) {
      add_space(temp, array, top, (int)s21_strlen(temp), variable);
    }
    write_into_main_buf(temp, array, top, (int)s21_strlen(temp), zero_flag, 0,
                        sign);
  }
  if (variable->align_minus) {
    align_left(array, top, (int)s21_strlen(temp) + variable->precision_zero,
               variable->width, variable, temp);
  }
  array[*top] = '\0';
  free(temp - temp_shift);
}
int add_precision_zero(char **temp, char *main_buf, int *top, params *variable,
                       int flag_x, int *shift) {
  int count = 0;
  if ((variable->width == 0) || (variable->align_minus == 1)) {
    if (((*temp)[0] != '-') && (variable->space_for_pos == 1)) {
      main_buf[*top] = ' ';
      *top += 1;
    } else if (((*temp)[0] != '-') && (variable->show_sign == 1)) {
      main_buf[*top] = '+';
      *top += 1;
    }
  }
  if (variable->precision_zero > 0 && flag_x == 0) {
    if ((*temp)[0] == '-') {
      main_buf[*top] = '-';
      *top += 1;
      for (int i = 0; i < variable->precision_zero; i++) {
        main_buf[*top] = '0';
        *top += 1;
        count++;
      }
      (*temp) += 1;
      (*shift) += 1;
    } else {
      for (int i = 0; i < variable->precision_zero; i++) {
        main_buf[*top] = '0';
        *top += 1;
      }
    }
  }
  if (variable->precision_zero > 0 && flag_x == 1) {
    if (variable->hash_zero) {
      main_buf[*top] = '0';
      *top += 1;
      main_buf[*top] = 'x';
      *top += 1;
    }
    for (int i = 0; i < variable->precision_zero; i++) {
      main_buf[*top] = '0';
      *top += 1;
      count++;
    }
  }
  return count;
}
void write_into_main_buf(const char *temp, char *main_buf, int *top, int count,
                         int flag, int hex_flag, int sign) {
  int i = 0;
  if (flag) {
    if (hex_flag) {
      i = 2;
    } else if (sign) {
      i = 1;
    }
  }
  for (; i < count; i++) {
    main_buf[*top] = temp[i];
    *top += 1;
  }
  main_buf[*top] = '\0';
}
void align_left(char *main_buf, int *top, int len, int fill, params *variable,
                const char *temp) {
  if (variable->show_sign == 1 && temp[0] != '-') {
    len++;
  }
  if ((variable->space_for_pos == 1) && (temp[0] != '-')) {
    len++;
  }
  if (fill > len) {
    for (int i = 0; i < (fill - len); i++) {
      main_buf[*top] = ' ';
      *top += 1;
    }
    main_buf[*top] = '\0';
  }
}
int add_zero(char **temp, char *main_buf, int *top, int len, params *variable,
             int *shift) {
  int count = 0;
  if (((*temp)[0] != '-') && (variable->show_sign == 1)) {
    len++;
    if (variable->width > 0) {
      main_buf[*top] = '+';
      *top += 1;
    }
  }
  if (variable->width > len) {
    if ((*temp)[0] == '-') {
      main_buf[*top] = '-';
      *top += 1;
      for (int i = 0; i < (variable->width - len); i++) {
        main_buf[*top] = '0';
        *top += 1;
        count++;
      }
      (*temp) += 1;
      (*shift) += 1;
    } else {
      for (int i = 0; i < (variable->width - len); i++) {
        main_buf[*top] = '0';
        *top += 1;
      }
    }
  }
  return count;
}
void add_space_precision_zero(char *temp, char *main_buf, int *top,
                              params *variable) {
  int len = 0;
  if (variable->show_sign == 1 && temp[0] != '-') {
    len++;
  }
  len = variable->width - variable->precision_zero - s21_strlen(temp) - len;
  if (len > 0) {
    for (int i = 0; i < len; i++) {
      main_buf[*top] = ' ';
      *top += 1;
    }
    if ((temp[0] != '-') && (variable->show_sign == 1)) {
      main_buf[*top] = '+';
      *top += 1;
    }
  } else if ((temp[0] != '-') && (variable->space_for_pos == 1)) {
    main_buf[*top] = ' ';
    *top += 1;
  } else if ((temp[0] != '-') && (variable->show_sign == 1)) {
    main_buf[*top] = '+';
    *top += 1;
  }
}
void add_space(const char *temp, char *main_buf, int *top, int len,
               params *variable) {
  if (variable->align_minus == 0) {
    if ((temp[0] != '-') && (variable->show_sign == 1)) {
      len++;
      if (variable->width <= len) {
        main_buf[*top] = '+';
        *top += 1;
      }
    }
    if (variable->width > len) {
      if (temp[0] == '-') {
        for (int i = 0; i < (variable->width - len); i++) {
          main_buf[*top] = ' ';
          *top += 1;
        }
      } else {
        for (int i = 0; i < (variable->width - len); i++) {
          main_buf[*top] = ' ';
          *top += 1;
        }
        if (variable->show_sign == 1) {
          main_buf[*top] = '+';
          *top += 1;
        }
      }
    } else if ((temp[0] != '-') && (variable->space_for_pos == 1)) {
      main_buf[*top] = ' ';
      *top += 1;
    }
  } else {
    if ((temp[0] != '-') && (variable->space_for_pos == 1)) {
      main_buf[*top] = ' ';
      *top += 1;
    } else if ((temp[0] != '-') && (variable->show_sign == 1)) {
      main_buf[*top] = '+';
      *top += 1;
    }
  }
}
int parse_params(const char *str_pointer, params *variable, int *shift) {
  *shift += 1;
  int local_stop_flag = 0;
  while (!local_stop_flag) {
    str_pointer++;
    if (*str_pointer == '-') {
      variable->align_minus = 1;
    } else if (*str_pointer == '+') {
      variable->show_sign = 1;
    } else if (*str_pointer == ' ') {
      variable->space_for_pos = 1;
    } else if (*str_pointer == '#') {
      variable->hash_zero = 1;
    } else if (*str_pointer >= 48 && *str_pointer <= 57) {
      if (*str_pointer == '0') {
        if (variable->dot_check == 0) {
          if (variable->direct_zero == 0 && variable->width == 0) {
            variable->direct_zero = 1;
          } else {
            variable->width = variable->width * 10;
          }
        } else {
          variable->precision_num =
              (variable->precision_num > 0)
                  ? (variable->precision_num * 10 + (*str_pointer - '0'))
                  : ((*str_pointer) - '0');
        }
      } else {
        if (variable->dot_check == 1) {
          variable->precision_num =
              (variable->precision_num > 0)
                  ? (variable->precision_num * 10 + (*str_pointer - '0'))
                  : ((*str_pointer) - '0');
        } else {
          variable->width =
              (variable->width > 0)
                  ? ((variable->width * 10) + (*str_pointer - '0'))
                  : (*str_pointer) - '0';
        }
      }
    } else if ((*str_pointer) == '.' || (*str_pointer) == ',') {
      variable->dot_check = 1;
    } else if (*str_pointer == '*') {
      if (variable->dot_check == 1) {
        variable->star_precision = 1;
      } else {
        variable->star_width = 1;
      }
    } else if (*str_pointer == 'h') {
      variable->len_h = 1;
    } else if (*str_pointer == 'l') {
      variable->len_l = 1;
    } else if (*str_pointer == 'L') {
      variable->len_double = 1;
    } else if (s21_strchr(TOKENS, (int)(*str_pointer)) ||
               (*str_pointer == '%')) {
      break;
    } else {
      local_stop_flag = 1;
    }
    *shift += 1;
  }
  return local_stop_flag;
}
void init_struct(params *res) {
  res->align_minus = 0;
  res->show_sign = 0;
  res->space_for_pos = 0;
  res->hash_zero = 0;
  res->direct_zero = 0;
  res->width = 0;
  res->star_width = 0;
  res->star_precision = 0;
  res->dot_check = 0;
  res->precision_num = -1;
  res->precision_zero = 0;
  res->len_h = 0;
  res->len_l = 0;
  res->len_double = 0;
}
char *s21_itoa(long int num) {
  char *res = malloc(sizeof(char) * 40);
  if (!res) exit(0);
  char *reverse = malloc(sizeof(char) * 40);
  if (!reverse) {
    free(res);
    exit(0);
  }
  int count = 0;
  int sign = 0;
  if (num < 0) {
    sign = 1;
    num *= -1;
  }
  if (num == 0) {
    res[count++] = '0';
    res[count++] = '\0';
  } else {
    int i;
    while (num > 0) {
      long int next = num % 10;
      reverse[count++] = '0' + next;
      num /= 10;
    }
    if (sign) {
      reverse[count++] = '-';
    }
    for (i = 0; i < count; i++) {
      res[i] = reverse[count - i - 1];
    }
    res[i] = '\0';
  }
  free(reverse);
  return res;
}
void delete_zero(char *g_string, int *top) {
  while (g_string[(*top) - 1] == '0') {
    g_string[(*top) - 1] = '\0';
    (*top) -= 1;
  }
  if (g_string[(*top) - 1] == conflicting_char) {
    g_string[(*top) - 1] = '\0';
    (*top) -= 1;
  }
}
char *hex_to_string(unsigned long int num, int upper_flag, int pointer_flag,
                    int nil_flag) {
  char *res = malloc(sizeof(char) * 50);
  if (!res) exit(0);
  char *reverse = malloc(sizeof(char) * 50);
  if (!reverse) {
    free(res);
    exit(0);
  }
  if (num == 0) {
    if (nil_flag) {
      for (int i = 0; i < 3; i++) {
        res[i] = "0x0"[i];
      }
      res[3] = '\0';
    } else {
      res[0] = '0';
      res[1] = '\0';
    }
  } else {
    int count = 0;
    int i = 0;
    while (num > 0) {
      long int next = num % 16;
      if (next > 9) {
        if (upper_flag) {
          reverse[count++] = 'A' + next - 10;
        } else {
          reverse[count++] = 'a' + next - 10;
        }
      } else {
        reverse[count++] = next + '0';
      }
      num /= 16;
    }
    reverse[count] = '\0';
    char *first = s21_strstr(reverse, "ffffffff");
    char *second = s21_strstr(reverse, "FFFFFFFF");
    if (first != S21_NULL || second != S21_NULL) {
      count = count - 8;
    }
    if (pointer_flag) {
      if (upper_flag) {
        reverse[count++] = 'X';
        reverse[count++] = '0';
      } else {
        reverse[count++] = 'x';
        reverse[count++] = '0';
      }
    }
    for (; i < count; i++) {
      res[i] = reverse[count - i - 1];
    }
    res[i] = '\0';
  }
  free(reverse);
  return res;
}
char *float_to_string(long double num, int g_flag, params *variable) {
  char *res = malloc(sizeof(char) * 50);
  if (!res) exit(0);
  char *reverse = S21_NULL;
  int top = 0;
  int loc_precision = variable->precision_num;
  int sign_flag = 0;

  if (num < 0) {
    res[top] = '-';
    num *= -1;
    top++;
    sign_flag = 1;
  }
  if (num != 0 && log10(num) >= 0) {
    reverse = s21_itoa((long int)num);
    for (int j = 0; j < (int)s21_strlen(reverse); j++) {
      res[top] = reverse[j];
      top++;
    }
    free(reverse);
  } else {
    res[top] = '0';
    top++;
  }
  res[top] = conflicting_char;
  top++;
  int fraction = check_fraction(&top, variable, num);
  long double int_part;
  long double frac_part = modfl(num, &int_part);
  if (fraction == 1) {
    int indicator = 0;
    long double next;
    for (int k = 0; k < (loc_precision + 1); k++) {
      frac_part *= 10;
      frac_part = modfl(frac_part, &next);
      res[top] = (int)next + '0';
      top++;
    }
    if (res[top - 1] >= 53) {
      res[top - 2] = ((res[top - 2] - '0') + 1) % 10 + '0';
      indicator++;
    }
    res[top - 1] = '\0';
    top--;
    if (indicator && (res[top - 1] == '0')) {
      int helper;
      int reminder = 1;
      for (int i = top - 2; i >= sign_flag; i--) {
        if (res[i] == '.' || res[i] == ',') {
          continue;
        }
        helper = reminder + res[i] - '0';
        res[i] = (helper % 10) + '0';
        reminder = helper / 10;
      }
    }
  } else {
    if ((long long int)round(num) - (long int)int_part > 0) {
      int helper;
      int reminder = 0;
      helper = reminder + res[top - 1] - '0';
      res[top - 1] = ((helper + 1) % 10) + '0';
      reminder = (helper + 1) / 10;
      for (int i = top - 2; i >= sign_flag; i--) {
        helper = reminder + res[i] - '0';
        res[i] = (helper % 10) + '0';
        reminder = helper / 10;
      }
    }
  }
  if (g_flag == 1 && variable->hash_zero == 0) {
    delete_zero(res, &top);
  }

  res[top] = '\0';
  top++;
  return res;
}
char *exp_to_string(long double v_e, const char *exp_letter, int g_flag,
                    params *variable) {
  char *res = malloc(sizeof(char) * 50);
  if (!res) exit(0);
  int top = 0;
  char exp_sign = '+';
  int loc_precision = variable->precision_num;
  char letter = (*exp_letter == 'E' || *exp_letter == 'G') ? 'E' : 'e';
  int main_sign = 0;

  if (v_e < 0) {
    res[top] = '-';
    v_e *= -1;
    top++;
    main_sign = 1;
  }
  int v_log = 0;
  if (v_e > 0) {
    v_log = find_exp(v_e);
  }
  if (v_e > 0 && v_e < 1) {
    exp_sign = '-';
  }
  long double num_to_save = (v_e / pow(10, v_log));
  res[top] = '0' + (int)num_to_save;
  top++;
  res[top] = conflicting_char;
  top++;
  long double int_part;
  long double frac_part = modfl(num_to_save, &int_part);
  int fraction = check_fraction(&top, variable, num_to_save);
  if (fraction == 1) {
    int indicator = 0;
    long double next;
    for (int i = 0; i < loc_precision + 1; i++) {
      frac_part *= 10;
      frac_part = modfl(frac_part, &next);
      res[top] = (int)next + '0';
      top++;
    }
    if (res[top - 1] >= 53) {
      res[top - 2] = ((res[top - 2] - '0') + 1) % 10 + '0';
      indicator++;
    }
    res[top - 1] = '\0';
    top--;
    if (indicator && (res[top - 1] == '0')) {
      int helper;
      int reminder = 1;
      for (int i = top - 2; i >= main_sign; i--) {
        if (res[i] == ',' || res[i] == '.') {
          continue;
        }
        helper = reminder + res[i] - '0';
        res[i] = (helper % 10) + '0';
        reminder = helper / 10;
      }
    }
    if (g_flag == 1 && variable->hash_zero == 0) {
      delete_zero(res, &top);
    }
  } else {
    if ((long long int)round(num_to_save) - (long int)int_part > 0) {
      int helper2 = res[0] - '0';
      res[0] = ((helper2 + 1) % 10) + '0';
    }
  }
  res[top] = letter;
  top++;
  res[top] = exp_sign;
  top++;
  if (v_log < 10 && v_log > -10) {
    res[top] = '0';
    top++;
  }
  char *exp_string = s21_itoa(v_log);
  int i = (v_log >= 0) ? 0 : 1;
  for (; i < (int)s21_strlen(exp_string); i++) {
    res[top] = exp_string[i];
    top++;
  }
  free(exp_string);
  res[top] = '\0';
  return res;
}
int check_fraction(int *top, params *variable, long double num) {
  int total;
  long int check = (long int)num;
  if ((num - check) == 0) {
    if (variable->precision_num == 0 && variable->dot_check == 1 &&
        variable->hash_zero == 1) {
      total = 0;
    } else if (variable->precision_num == 0 && variable->dot_check == 1 &&
               variable->hash_zero == 0) {
      total = 0;
      *top -= 1;
    } else {
      total = 1;
    }
  } else if (variable->dot_check == 1 && variable->precision_num == 0) {
    if (variable->hash_zero == 0) {
      total = 0;
      *top -= 1;
    } else {
      total = 0;
    }
  } else {
    total = 1;
  }
  return total;
}
int check_precision(params *variable, int expo) {
  int res = 2;
  if (variable->precision_num == 0) {
    if (expo < -4 || expo >= 6) {
      res = 1;
    }
  } else if (variable->precision_num > 0) {
    if (expo < -4 || expo >= variable->precision_num) {
      res = 1;
    }
  }
  return res;
}

/****** PART4 *****/


int s21_sscanf(const char *str, const char *format, ...) {
  setlocale(LC_ALL, "");
  setlocale(LC_NUMERIC, "en_US.UTF-8");
  int res = 0;
  flags fl = {0, 0, 0, 0, 0, '\0', 0, 0};
  char *strc = malloc((s21_strlen(str) + 1) * sizeof(char));
  if (!strc) exit(0);
  strc = s21_strcpy(strc, str);
  spaceTrim(&strc, &fl);
  if (!*strc) fl.eof = 1;
  strc = s21_strcpy(strc - fl.n, str);
  fl.n = 0;
  va_list args;
  va_start(args, format);
  for (; *format; format++) {
    if (flagsInv(&strc, &fl, format)) continue;
    if (fl.form) {
      if ((int)*format > 47 && (int)*format < 58) {
        fl.width = fl.width * 10 + (int)*format - 48;
        continue;
      }
      res += switchFormat(args, &fl, &strc, format);
    } else {
      caseNonFormat(&strc, &fl, format);
    }
    if (checkBreak(args, &fl, &strc, format)) {
      if (!res && fl.eof) res = -1;
      break;
    }
  }
  free(strc - fl.n);
  va_end(args);
  return res;
}
int caseInt(va_list args, flags *fl, char **strc, int sys) {
  int res = 0;
  char *strend;
  numericBuff(strc, fl);
  if (s21_strtol(*strc, S21_NULL, sys) ||
      *(*strc + s21_strspn(*strc, "\n\t \f\x0B\r+-")) == '0') {
    if (!fl->supr) {
      res++;
      if (fl->length == 1)
        *(short int *)va_arg(args, void *) = s21_strtol(*strc, &strend, sys);
      else if (fl->length == 2)
        *(long int *)va_arg(args, void *) = s21_strtol(*strc, &strend, sys);
      else
        *(int *)va_arg(args, void *) = s21_strtol(*strc, &strend, sys);
    } else {
      s21_strtol(*strc, &strend, sys);
    }
    fl->n += strend - *strc;
    *strc = strend;
  } else {
    fl->err = 1;
  }
  fl->form = 0;
  return res;
}
int caseUns(va_list args, flags *fl, char **strc, int sys) {
  int res = 0;
  char *strend;
  numericBuff(strc, fl);
  if (s21_strtoul(*strc, S21_NULL, sys) ||
      *(*strc + s21_strspn(*strc, "\n\t \f\x0B\r+")) == '0') {
    if (!fl->supr) {
      if (s21_strtoul(*strc, S21_NULL, sys) || **strc == '0') res++;
      if (fl->length == 1)
        *(short unsigned *)va_arg(args, void *) =
            s21_strtoul(*strc, &strend, sys);
      else if (fl->length == 2)
        *(long unsigned *)va_arg(args, void *) =
            s21_strtoul(*strc, &strend, sys);
      else
        *(unsigned *)va_arg(args, void *) = s21_strtoul(*strc, &strend, sys);
    } else {
      s21_strtoul(*strc, &strend, sys);
    }
    fl->n += strend - *strc;
    *strc = strend;
  } else {
    fl->err = 1;
  }
  fl->form = 0;
  return res;
}
int caseFlo(va_list args, flags *fl, char **strc) {
  int res = 0;
  char *strend;
  numericBuff(strc, fl);
  if (fabs(s21_strtod(*strc, S21_NULL)) >= 1e-100 ||
      isnan(s21_strtod(*strc, S21_NULL)) ||
      *(*strc + s21_strspn(*strc, "\n\t \f\x0B\r+-")) == '0') {
    if (!fl->supr) {
      res++;
      if (fl->length == 3)
        *(long double *)va_arg(args, void *) = s21_strtold(*strc, &strend);
      else if (fl->length == 2)
        *(double *)va_arg(args, void *) = s21_strtod(*strc, &strend);
      else
        *(float *)va_arg(args, void *) = s21_strtof(*strc, &strend);
    } else {
      s21_strtof(*strc, &strend);
    }
    fl->n += strend - *strc;
    *strc = strend;
  } else {
    fl->err = 1;
  }
  fl->form = 0;
  return res;
}
int casePtr(va_list args, flags *fl, char **strc) {
  int res = 0;
  char *strend;
  if (s21_strtoul(*strc, S21_NULL, 16) ||
      *(*strc + s21_strspn(*strc, "\n\t \f\x0B\r+-")) == '0') {
    numericBuff(strc, fl);
    if (!fl->supr) {
      if (s21_strtoul(*strc, S21_NULL, 16) || **strc == '0') res++;
      *(void **)va_arg(args, void **) = (void *)s21_strtoul(*strc, &strend, 16);
    } else {
      s21_strtoul(*strc, &strend, 16);
    }
    fl->n += strend - *strc;
    *strc = strend;
  } else {
    fl->err = 1;
  }
  fl->form = 0;
  return res;
}
int caseCha(va_list args, flags *fl, char **strc) {
  int res = 0;
  if (!fl->width) fl->width = 2;
  if (!fl->supr) {
    res++;
    if (fl->length == 2)
      mbtowc((wchar_t *)va_arg(args, wchar_t *), *strc, fl->width);
    else
      *(char *)va_arg(args, char *) = **strc;
  }
  if (**strc < 0 && fl->length == 2) {
    (*strc)++;
    fl->n++;
  }
  (*strc)++;
  fl->n++;
  fl->form = 0;
  return res;
}
int caseStr(va_list args, flags *fl, char **strc) {
  int res = 0;
  char *s = malloc(sizeof(char));
  if (!s) exit(0);
  spaceTrim(strc, fl);
  int i = 0;
  for (; **strc && **strc != ' ' && **strc != '\n' && **strc != '\t' &&
         **strc != '\r' && **strc != '\x0B' && **strc != '\f' &&
         (fl->width == 0 || i < fl->width);
       i++, (*strc)++) {
    s[i] = **strc;
    s = realloc(s, (i + 2) * sizeof(char));
    if (!s) exit(0);
  }
  s[i] = '\0';
  int k = s21_strlen(s) + 1;
  va_list s_list;
  va_copy(s_list, args);
  for (int j = 0; j < k; j++) {
    if (!fl->supr) {
      if (!fl->length) *((char *)va_arg(s_list, char *) + j) = s[j];
      if (j + 1 < k) {
        va_end(s_list);
        va_copy(s_list, args);
      }
    }
  }
  va_end(args);
  va_copy(args, s_list);
  if (fl->length == 2 && !fl->supr)
    mbstowcs((wchar_t *)va_arg(args, wchar_t *), s, k);
  free(s);
  if (!fl->supr) res++;
  fl->n += k - 1;
  fl->form = 0;
  va_end(s_list);
  return res;
}
void spaceTrim(char **strc, flags *fl) {
  while (**strc == ' ' || **strc == '\n' || **strc == '\t' || **strc == '\r' ||
         **strc == '\x0B' || **strc == '\f') {
    (*strc)++;
    fl->n++;
  }
}
void casePer(char **strc, flags *fl, const char *format) {
  spaceTrim(strc, fl);
  if (*format == **strc) {
    fl->n++;
    (*strc)++;
  } else {
    fl->err = 1;
  }
  fl->form = 0;
}
int flagsInv(char **strc, flags *fl, const char *format) {
  int res = 0;
  if (*format == '%' && !fl->form) {
    res++;
    fl->form = 1;
    fl->supr = 0;
    fl->length = 0;
    if (fl->buff) {
      *(*strc + s21_strlen(*strc)) = fl->buff;
      fl->buff = '\0';
    }
    fl->width = 0;
  }
  return res;
}
void caseN(va_list args, flags *fl) {
  if (!fl->supr) {
    if (fl->length == 1)
      *(short int *)va_arg(args, void *) = fl->n;
    else if (fl->length == 2)
      *(long int *)va_arg(args, void *) = fl->n;
    else
      *(int *)va_arg(args, void *) = fl->n;
  }
  fl->form = 0;
}
void caseNonFormat(char **strc, flags *fl, const char *format) {
  if (*format == ' ' || *format == '\t' || *format == '\n' || *format == '\r' ||
      *format == '\x0B') {
    while (*format == **strc) {
      (*strc)++;
      fl->n++;
    }
  } else if (**strc == *format) {
    (*strc)++;
    fl->n++;
  } else {
    fl->err = 1;
  }
}
int checkBreak(va_list args, flags *fl, char **strc, const char *format) {
  int res = 0;
  va_list backup;
  va_copy(backup, args);
  if ((!**strc && !fl->buff &&
       (s21_strstr(format, "%n") != s21_strchr(format, '%') ||
        !s21_strstr(format, "%n"))) ||
      !va_arg(backup, void *) || fl->err) {
    res = 1;
  }
  va_end(backup);
  return res;
}
int switchFormat(va_list args, flags *fl, char **strc, const char *format) {
  int res = 0;
  switch (*format) {
    case 'x':
    case 'X':
      res += caseUns(args, fl, strc, 16);
      break;
    case 'p':
      res += casePtr(args, fl, strc);
      break;
    case 'e':
    case 'E':
    case 'f':
    case 'g':
    case 'G':
      res += caseFlo(args, fl, strc);
      break;
    case 'c':
      res += caseCha(args, fl, strc);
      break;
    case 'd':
      res += caseInt(args, fl, strc, 10);
      break;
    case 'i':
      res += caseInt(args, fl, strc, 0);
      break;
    case 'o':
      res += caseUns(args, fl, strc, 8);
      break;
    case 's': {
      res += caseStr(args, fl, strc);
      break;
    }
    case 'u':
      res += caseUns(args, fl, strc, 10);
      break;
    case 'n':
      caseN(args, fl);
      break;
    case '%':
      casePer(strc, fl, format);
      break;
    case '*':
      fl->supr = 1;
      break;
    case 'h':
      fl->length = 1;
      break;
    case 'l':
      fl->length = 2;
      break;
    case 'L':
      fl->length = 3;
      break;
  }
  return res;
}
void numericBuff(char **strc, flags *fl) {
  spaceTrim(strc, fl);
  if (fl->width && !fl->buff && fl->width < (int)s21_strlen(*strc)) {
    fl->buff = *(*strc + fl->width);
    *(*strc + fl->width) = '\0';
  }
}
long s21_strtol(char *str, char **strend, int sys) {
  char *start = str;
  long int res = 0;
  int minus = 1;
  while (*str == ' ' || *str == '\n' || *str == '\t' || *str == '\r' ||
         *str == '\x0B' || *str == '\f')
    str++;
  if (*str == '+') str++;
  if (*str == '-') {
    minus = -1;
    str++;
  }
  if (sys == 0 && *str == '0' && *(str + 1) == 'x')
    sys = 16;
  else if (sys == 0 && *str == '0')
    sys = 8;
  else if (sys == 0)
    sys = 10;
  if (sys == 16 && *str == '0' && *(str + 1) == 'x') str += 2;
  if (sys == 10) {
    for (; *str > 47 && *str < 58; str++, res *= 10) res += *str - 48;
    res /= 10;
  } else if (sys == 8) {
    for (; *str > 47 && *str < 56; str++, res *= 8) res += *str - 48;
    res /= 8;
  } else if (sys == 16) {
    for (; (*str > 47 && *str < 58) || (*str > 64 && *str < 71) ||
           (*str > 96 && *str < 103);
         str++, res *= 16) {
      if (*str > 47 && *str < 58)
        res += *str - 48;
      else if ((*str > 64 && *str < 71))
        res += +*str - 55;
      else
        res += +*str - 87;
    }
    res /= 16;
  }
  if (strend) *strend = start + (str - start);
  return minus * res;
}
unsigned long s21_strtoul(char *str, char **strend, int sys) {
  return s21_strtol(str, strend, sys);
}
float s21_strtof(char *str, char **strend) {
  char *start = str;
  float a, decplace, b;
  int sign = 1;
  while (*str == ' ' || *str == '\n' || *str == '\t' || *str == '\r' ||
         *str == '\x0B' || *str == '\f')
    ++str;
  if (*str == '+') ++str;
  if (*str == '-') {
    sign = -1;
    ++str;
  }
  for (a = 0; *str && isdigit(*str); ++str) a = a * 10 + (*str - '0');
  if (*str == '.') ++str;
  for (decplace = 1.; *str && isdigit(*str); ++str, decplace *= 10.)
    a = a * 10. + (*str - '0');
  if (*str == 'e' || *str == 'E') {
    int bsign = 1;
    if (a <= 1e-6) a = 1;
    ++str;
    if (*str == '-') {
      bsign = -1;
      ++str;
    }
    if (*str == '+') ++str;
    for (b = 0; *str && isdigit(*str); ++str) b = b * 10 + (*str - '0');
    b *= bsign;
  } else {
    b = 0;
  }
  if ((*str == 'n' || *str == 'N') && (str[1] == 'a' || str[1] == 'A') &&
      (str[2] == 'n' || str[2] == 'N')) {
    str += 3;
    a = NAN * sign;
  }
  if ((*str == 'i' || *str == 'I') && (str[1] == 'n' || str[1] == 'N') &&
      (str[2] == 'f' || str[2] == 'F')) {
    str += 3;
    a = INFINITY * sign;
  }
  if (strend) *strend = start + (str - start);
  return (isnan(a) || isinf(a)) ? a : (a * sign / decplace) * powl(10, b);
}
double s21_strtod(char *str, char **strend) {
  char *start = str;
  double a, decplace, b;
  int sign = 1;
  while (*str == ' ' || *str == '\n' || *str == '\t' || *str == '\r' ||
         *str == '\x0B' || *str == '\f')
    ++str;
  if (*str == '+') ++str;
  if (*str == '-') {
    sign = -1;
    ++str;
  }
  for (a = 0; *str && isdigit(*str); ++str) a = a * 10 + (*str - '0');
  if (*str == '.') ++str;
  for (decplace = 1.; *str && isdigit(*str); ++str, decplace *= 10.)
    a = a * 10. + (*str - '0');
  if (*str == 'e' || *str == 'E') {
    int bsign = 1;
    if (a <= 1e-6) a = 1;
    ++str;
    if (*str == '-') {
      bsign = -1;
      ++str;
    }
    if (*str == '+') ++str;
    for (b = 0; *str && isdigit(*str); ++str) b = b * 10 + (*str - '0');
    b *= bsign;
  } else {
    b = 0;
  }
  if ((*str == 'n' || *str == 'N') && (str[1] == 'a' || str[1] == 'A') &&
      (str[2] == 'n' || str[2] == 'N')) {
    str += 3;
    a = NAN * sign;
  }
  if ((*str == 'i' || *str == 'I') && (str[1] == 'n' || str[1] == 'N') &&
      (str[2] == 'f' || str[2] == 'F')) {
    str += 3;
    a = INFINITY * sign;
  }
  if (strend) *strend = start + (str - start);
  return (isnan(a) || isinf(a)) ? a : (a * sign / decplace) * powl(10, b);
}
long double s21_strtold(char *str, char **strend) {
  char *start = str;
  long double a, decplace, b;
  int sign = 1;
  while (*str == ' ' || *str == '\n' || *str == '\t' || *str == '\r' ||
         *str == '\x0B' || *str == '\f')
    ++str;
  if (*str == '+') ++str;
  if (*str == '-') {
    sign = -1;
    ++str;
  }
  for (a = 0; *str && isdigit(*str); ++str) a = a * 10 + (*str - '0');
  if (*str == '.') ++str;
  for (decplace = 1.; *str && isdigit(*str); ++str, decplace *= 10.)
    a = a * 10. + (*str - '0');
  if (*str == 'e' || *str == 'E') {
    int bsign = 1;
    if (a <= 1e-6) a = 1;
    ++str;
    if (*str == '-') {
      bsign = -1;
      ++str;
    }
    if (*str == '+') ++str;
    for (b = 0; *str && isdigit(*str); ++str) b = b * 10 + (*str - '0');
    b *= bsign;
  } else {
    b = 0;
  }
  if ((*str == 'n' || *str == 'N') && (str[1] == 'a' || str[1] == 'A') &&
      (str[2] == 'n' || str[2] == 'N')) {
    str += 3;
    a = NAN * sign;
  }
  if ((*str == 'i' || *str == 'I') && (str[1] == 'n' || str[1] == 'N') &&
      (str[2] == 'f' || str[2] == 'F')) {
    str += 3;
    a = INFINITY * sign;
  }
  if (strend) *strend = start + (str - start);
  return (isnan(a) || isinf(a)) ? a : (a * sign / decplace) * powl(10, b);
}

/****** PART5 *****/

void *s21_insert(const char *src, const char *str, s21_size_t start_index) {
    int check = 0;
    char *man = S21_NULL;
    if (src && str && s21_strlen(src) >= start_index) {
        s21_size_t begin = s21_strlen(src);
        s21_size_t end = s21_strlen(str);
        s21_size_t insert = 0;
        man = (char *)malloc((begin + end + 1) * sizeof(char));
        for (s21_size_t a = 0; a < begin + end; a++) {
            if (a == start_index) {
                for (s21_size_t b = 0; b < end; b++) {
                    man[insert] = str[b];
                    insert++;
                }
            }
            man[insert] = src[a];
            insert++;
        }
    } else {
        check = 1;
    }
    return check == 0 ? man : S21_NULL;
}
void *s21_to_lower(const char *str) {
    char *new_str = S21_NULL;
    if (str) {
        new_str = (char *)malloc((s21_strlen(str) + 1) * sizeof(char));
    }
    if (new_str) {
        s21_strncpy(new_str, str, s21_strlen(str) + 1);
        for (char *lower = new_str; *lower; lower++) {
            if (*lower >= 'A' && *lower <= 'Z') {
                *lower += 32;
            }
        }
    }
    return (void *)new_str;
}
void *s21_to_upper(const char *str) {
    char *new_str = S21_NULL;
    if (str) {
        new_str = (char *)malloc((s21_strlen(str) + 1) * sizeof(char));
    }
    if (new_str) {
        s21_strncpy(new_str, str, s21_strlen(str) + 1);
        for (char *upper = new_str; *upper; upper++) {
            if (*upper >= 'a' && *upper <= 'z') {
                *upper -= 32;
            }
        }
    }
    return (void *)new_str;
}
static size_t s21_strlcpy(char *dest, const char *src, s21_size_t size) {
    s21_size_t i = 0;

    while (size > 1 && src[i] != '\0') {
        dest[i] = src[i];
        i++;
        size--;
    }
    if (size != 0) {
        dest[i] = '\0';
    }
    while (src[i] != '\0') {
        i++;
    }
    return i;
}
void *s21_trim(const char *src, const char *trim_chars) {
    char *result;
    char *str;
    s21_size_t start;
    s21_size_t end;
    s21_size_t buf_size;

    str = (char *)src;
    result = S21_NULL;
    if (src != S21_NULL && trim_chars != S21_NULL) {
        start = 0;
        end = s21_strlen(src);
        while (src[start] && s21_strchr(trim_chars, src[start])) {
            ++start;
        }
        while (src[end - 1] && s21_strchr(trim_chars, src[end - 1]) && end > start) {
            --end;
        }
        buf_size = end - start + 1;
        result = (char *)malloc(sizeof(char) * (buf_size));
        if (result) {
            s21_strlcpy(result, &str[start], (buf_size));
        }
    }
    return result;
}
