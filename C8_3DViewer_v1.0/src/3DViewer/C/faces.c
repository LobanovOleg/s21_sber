#include "faces.h"

void faces_default(faces_t *faces) {
  faces->array_faces = NULL;
  faces->capacity = 0;
  faces->size = 0;
}

void free_faces(faces_t *faces) {
  if (faces) {
    free(faces->array_faces);
    faces_default(faces);
  }
}

my_error_t save_face(const face_t *face, FILE *fout) {
  int rc = SUCCESS;

  for (int i = 0; i < face->size; ++i) {
    rc = fprintf(fout, "%d ", face->points[i]);
    if (rc) break;
  }
  if (0 > rc) return FILE_WRITE_ERROR;
  rc = fprintf(fout, "\n");
  if (0 > rc) return FILE_WRITE_ERROR;
  return SUCCESS;
}

my_error_t save_all_faces(const faces_t *faces, FILE *fout) {
  my_error_t rc = SUCCESS;
  if (fprintf(fout, "f ") < 0)
    rc = FILE_WRITE_ERROR;
  else
    for (int i = 0; rc == SUCCESS && i < faces->size; i++)
      rc = save_face(&faces->array_faces[i], fout);

  return rc;
}

void *my_faces_points_realloc(face_t *face, int new_size) {
  if (new_size > face->capacity) {
    int new_capacity = (face->capacity == 0) ? 1 : face->capacity * 2;
    while (new_size > new_capacity) {
      new_capacity *= 2;
    }
    if (face->points == NULL)
      face->points = (int *)malloc(new_capacity * sizeof(int));
    else
      face->points = (int *)realloc(face->points, new_capacity * sizeof(int));
    face->capacity = new_capacity;
  }

  return face->points;
}

my_error_t append_face_point(face_t *face, int point) {
  int rc = SUCCESS;
  if (face->size == face->capacity) {
    face->points = (int *)my_faces_points_realloc(face, face->size + 1);
    if (!face->points) rc = MEMORY_ALLOCATE_ERROR;
  }
  if (!rc) {
    face->points[face->size] = point;
    face->size++;
  }
  return rc;
}

void *my_faces_realloc(faces_t *faces, int new_size) {
  if (new_size > faces->capacity) {
    int new_capacity = (faces->capacity == 0) ? 1 : faces->capacity * 2;
    while (new_size > new_capacity) {
      new_capacity *= 2;
    }
    if (faces->array_faces == NULL)
      faces->array_faces = (face_t *)malloc(new_capacity * sizeof(face_t));
    else
      faces->array_faces =
          (face_t *)realloc(faces->array_faces, new_capacity * sizeof(face_t));
    faces->capacity = new_capacity;
  }

  return faces->array_faces;
}

my_error_t append_face(faces_t *faces, face_t face) {
  int rc = SUCCESS;
  if (faces->size == faces->capacity) {
    faces->array_faces = (face_t *)my_faces_realloc(faces, faces->size + 1);
    if (!faces->array_faces) rc = MEMORY_ALLOCATE_ERROR;
  }
  if (!rc) {
    faces->array_faces[faces->size] = face;
    faces->size++;
  }
  return rc;
}
