#ifndef POINT_H
#define POINT_H

#ifdef __cplusplus
extern "C" {
#endif

#include "action_data.h"
#include "errors.h"
#include "math.h"
#include "stdio.h"
#include "stdlib.h"

typedef struct point {
  double x;
  double y;
  double z;
  int *pairs;
  int size;
} point_t;

void point_default(point_t *point);
void move_point(point_t *point, const move_t *move);
void rotate_point(point_t *point, const point_t *r_center,
                  const rotate_t *rotate);
void scale_point(point_t *point, const point_t *s_center, const scale_t *scale);
my_error_t save_point(const point_t *point, FILE *fout);

#ifdef __cplusplus
}
#endif

#endif  // POINT_H
