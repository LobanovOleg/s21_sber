#ifndef FIGURE_H
#define FIGURE_H

#ifdef __cplusplus
extern "C" {
#endif

#include "action_data.h"
#include "edges.h"
#include "errors.h"
#include "faces.h"
#include "points.h"
#include "stdio.h"
#include "stdlib.h"
#include "string.h"

typedef struct figure {
  point_t center;
  points_t points;
  edges_t edges;
  faces_t faces;
} figure_t;

figure_t* figure_init(void);

void free_figure(figure_t* figure);
my_error_t fread_figure(figure_t* figure, FILE* fin);
my_error_t download_figure(figure_t* figure, const char* filename);
my_error_t move_figure(figure_t* figure, const move_t* move);
my_error_t scale_figure(figure_t* figure, const scale_t* scale);
my_error_t rotate_figure(figure_t* figure, const rotate_t* rotate);
my_error_t save_figure(const figure_t* figure, const char* filename);
my_error_t face_to_edges(const face_t* face, edges_t* edges,
                         int** points_table);
int exist_edge(const edge_t* edge, int** points_table);

#ifdef __cplusplus
}
#endif

#endif  // FIGURE_H
