#include "points.h"

void points_default(points_t* points) {
  points->array_points = NULL;
  points->points_table = NULL;
  points->capacity = 0;
  points->size = 0;
}

void find_min_max_points(points_t* points, double* min_x, double* max_x,
                         double* min_y, double* max_y, double* min_z,
                         double* max_z) {
  if (!points || !points->array_points) return;
  *min_x = points->array_points[0].x;
  *max_x = points->array_points[0].x;
  *min_y = points->array_points[0].y;
  *max_y = points->array_points[0].y;
  *min_z = points->array_points[0].z;
  *max_z = points->array_points[0].z;
  for (int i = 1; i < points->size; ++i) {
    if (points->array_points[i].x < *min_x) *min_x = points->array_points[i].x;
    if (points->array_points[i].x > *max_x) *max_x = points->array_points[i].x;

    if (points->array_points[i].y < *min_y) *min_y = points->array_points[i].y;
    if (points->array_points[i].y > *max_y) *max_y = points->array_points[i].y;

    if (points->array_points[i].z < *min_z) *min_z = points->array_points[i].z;
    if (points->array_points[i].z > *max_z) *max_z = points->array_points[i].z;
  }
}

void free_points(points_t* points) {
  if (points) {
    for (int i = 0; i < points->size; i++) {
      free(points->points_table[i]);
    }
    free(points->points_table);
    free(points->array_points);
    points_default(points);
  }
}

void* my_points_realloc(points_t* points, int new_size) {
  if (new_size > points->capacity) {
    int new_capacity = (points->capacity == 0) ? 1 : points->capacity * 2;
    while (new_size > new_capacity) {
      new_capacity *= 2;
    }
    if (points->array_points == NULL)
      points->array_points = (point_t*)malloc(new_capacity * sizeof(point_t));
    else
      points->array_points = (point_t*)realloc(points->array_points,
                                               new_capacity * sizeof(point_t));
    points->capacity = new_capacity;
  }

  return points->array_points;
}

my_error_t append_point(points_t* points, point_t point) {
  int rc = SUCCESS;
  if (points->size == points->capacity) {
    points->array_points =
        (point_t*)my_points_realloc(points, points->size + 1);
    if (!points->array_points) rc = MEMORY_ALLOCATE_ERROR;
  }
  if (!rc) {
    points->array_points[points->size] = point;
    points->size++;
  }
  return rc;
}

my_error_t move_all_points(points_t* points, const move_t* coeff) {
  if (!points->array_points) return FIGURE_NOT_LOADED;

  for (int i = 0; i < points->size; i++)
    move_point(&points->array_points[i], coeff);

  return SUCCESS;
}

my_error_t rotate_all_points(points_t* points, const point_t* r_center,
                             const rotate_t* coeff) {
  if (!points->array_points) return FIGURE_NOT_LOADED;

  for (int i = 0; i < points->size; i++)
    rotate_point(&points->array_points[i], r_center, coeff);

  return SUCCESS;
}

my_error_t scale_all_points(points_t* points, const point_t* s_center,
                            const scale_t* coeff) {
  my_error_t rc = SUCCESS;
  if (!points->array_points)
    rc = FIGURE_NOT_LOADED;
  else if (coeff->kx <= 0 || coeff->ky <= 0 || coeff->kz <= 0)
    rc = COEFF_SCALE_ERROR;
  else
    for (int i = 0; i < points->size; i++)
      scale_point(&points->array_points[i], s_center, coeff);

  return rc;
}

my_error_t save_all_points(const points_t* points, FILE* fout) {
  my_error_t rc = SUCCESS;
  for (int i = 0; rc == SUCCESS && i < points->size; i++)
    rc = save_point(&points->array_points[i], fout);

  return rc;
}
