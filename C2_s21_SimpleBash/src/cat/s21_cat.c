#include <stdio.h>
#include <string.h>

#ifndef ERROR
#define ERROR 0
#endif

struct Keys {
    int b;
    int s;
    int e;
    int t;
    int n;
    int v;
};

void print_key(struct Keys key);
int parsing_keys(int argc, char **argv, struct Keys *key, int *error);
void openF(int argc, char **argv, int count, struct Keys key);
void print_on_screen(FILE *fn, struct Keys key);
void print_argumets(int argc, char **argv);

int main(int argc, char **argv) {
  int error = 0;
  if (argc > 1) {
    struct Keys key = {
      .b = 0,
      .e = 0,
      .n = 0,
      .s = 0,
      .t = 0,
      .v = 0,
    };
    int count = parsing_keys(argc, argv, &key, &error);
    if (!error) {
      openF(argc, argv, count, key);
    }
  }
  return error;
}

int parsing_keys(int argc, char **argv, struct Keys *key, int *error) {
  int i = 0;
  for (int c = 1; c < argc; c++) {
    if (argv[c][0] == '-' && argv[c][1] == '-') {
      if (!strcmp(argv[c], "--number-nonblank")) {
        key->b = 1;
        argv[c] = "\0";
      } else if (!strcmp(argv[c], "--number")) {
        key->n = 1;
        argv[c] = "\0";
      } else if (!strcmp(argv[c], "--squeeze-blank")) {
        key->s = 1;
        argv[c] = "\0";
      } else {
        *error = 1;
        fprintf(stderr, "s21_cat: illegal keyion -- -\nusae: s21_cat [-benstuv] [file...]\n");
      }
    } else if (argv[c][0] == '-') {
      for (int a = 1; a < (int)strlen(argv[c]); a++) {
        switch (argv[c][a]) {
          case 'b':
            key->b = 1;
            break;
          case 'n':
            key->n = 1;
            break;
          case 's':
            key->s = 1;
            break;
          case 'v':
            key->v = 1;
            break;
          case 't':
            key->t = 1;
            key->v = 1;
            break;
          case 'e':
            key->e = 1;
            key->v = 1;
            break;
          case 'E':
            key->e = 1;
            break;
          case 'T':
            key->t = 1;
            break;
          default:
            *error = 1;
            fprintf(stderr, "cat: illegal option -- %c\nusage: cat [-benstuv] [file...]\n", argv[c][a]);
        }
      }
    } else {
      i = c;
      break;
    }
  }
  if (key->b) {
    key->n = 0;
  }
  return i;
}

void openF(int argc, char **argv, int count, struct Keys key) {
  FILE *fn;
  int check = 0;
  if (check == 1) {
    printf("\t");
  }
  while (count < argc) {
    fn = fopen(argv[count], "r");
    if (fn == NULL) {
      fprintf(stderr, "s21_cat: %s:No such a file or directory\n", argv[count]);
      break;
    } else {
      print_on_screen(fn, key);
      check = 1;
      fclose(fn);
    }
    count++;
  }
}

void print_on_screen(FILE *fn, struct Keys key) {
  char fut = '\0';
  char prnt = fgetc(fn);
  if (prnt != EOF) {
    int line = 1;
    int check = 1;
    if (key.b && prnt != '\n') {
      printf("%6d\t", line);
    }
    if (key.n) {
      printf("%6d\t", line);
    }
    if (key.e && prnt == '\n') {
      printf("$");
    }
    while (fut != EOF) {
      fut = fgetc(fn);
      if (key.s && prnt == '\n' && fut == '\n') {
        while (fut == '\n') {
          fut = fgetc(fn);
        }
        if (!check) {
          printf("\n");
        }
        if (key.n) {
          line++;
          printf("%6d\t", line);
        }
        if (key.e) {
          printf("$");
        }
      }
      check = 0;
      if (key.v && (0 <= (int)prnt) && ((int)prnt < 32) && prnt != '\n' && prnt != '\t') {
        printf("^%c", (int)prnt + 64);
      } else if ((int)prnt == 127 && key.v) {
        printf("^%c", (int)prnt - 64);
      } else if (key.t && prnt == '\t') {
        printf("^I");
      } else {
        printf("%c", prnt);
      }
      if ((key.b && prnt == '\n' && fut != '\n') || (key.n && prnt == '\n' && fut != EOF)) {
        line++;
        printf("%6d\t", line);
      }
      if (key.e && key.b && fut == '\n' && prnt == '\n') {
        printf("\t$");
      }
      else if (key.e && fut == '\n') {
        printf("$");
      } 
      prnt = fut;
    }
  }
}

void print_key(struct Keys key) {
  printf(
    "b = %d\nn = %d\ns = %d\nv = %d\ne = %d\nt = %d\n",
    key.b, key.n, key.s, key.v, key.e, key.t);
}

void print_arguments(int argc, char **argv) {
  printf("%d\n", argc);
  for (int count = 1; count < argc; count++) {
    printf("%s\n", argv[count]);
  }
}