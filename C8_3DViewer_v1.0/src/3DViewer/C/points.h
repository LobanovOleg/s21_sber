#ifndef POINTS_H
#define POINTS_H

#ifdef __cplusplus
extern "C" {
#endif

#include "errors.h"
#include "point.h"
#include "stdio.h"
#include "stdlib.h"

typedef struct points {
  point_t *array_points;
  int size;
  int capacity;
  int **points_table;
} points_t;

void points_default(points_t *points);
void free_points(points_t *points);
my_error_t move_all_points(points_t *points, const move_t *coeff);
my_error_t rotate_all_points(points_t *points, const point_t *r_center,
                             const rotate_t *coeff);
my_error_t scale_all_points(points_t *points, const point_t *s_center,
                            const scale_t *coeff);
my_error_t save_all_points(const points_t *points, FILE *fout);
my_error_t append_point(points_t *points, point_t point);
void find_min_max_points(points_t *points, double *min_x, double *max_x,
                         double *min_y, double *max_y, double *min_z,
                         double *max_z);

#ifdef __cplusplus
}
#endif

#endif  // POINTS_H
