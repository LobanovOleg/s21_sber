#ifndef ACTION_DATA_H
#define ACTION_DATA_H

#ifdef __cplusplus
extern "C" {
#endif

typedef struct move {
  double dx;
  double dy;
  double dz;
} move_t;

typedef struct rotate {
  double angle_x;
  double angle_y;
  double angle_z;
} rotate_t;

typedef struct scale {
  double kx;
  double ky;
  double kz;
} scale_t;

#ifdef __cplusplus
}
#endif

#endif  // ACTION_DATA_H
