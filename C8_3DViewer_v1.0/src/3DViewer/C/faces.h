#ifndef FACES_H
#define FACES_H

#ifdef __cplusplus
extern "C" {
#endif

#include "points.h"

typedef struct face {
  int *points;
  int size;
  int capacity;
} face_t;

typedef struct faces {
  face_t *array_faces;
  int size;
  int capacity;
} faces_t;

void free_faces(faces_t *faces);
void faces_default(faces_t *faces);
my_error_t save_all_faces(const faces_t *faces, FILE *fout);
my_error_t save_face(const face_t *face, FILE *fout);
my_error_t append_face(faces_t *faces, face_t face);
my_error_t append_face_point(face_t *face, int point);

#ifdef __cplusplus
}
#endif

#endif  // FACES_H
