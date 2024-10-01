#ifndef EDGES_H
#define EDGES_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdio.h>
#include <stdlib.h>

#include "errors.h"
#include "points.h"

typedef struct edge {
  int first_point;
  int second_point;
} edge_t;

typedef struct edges {
  edge_t *array_edges;
  int last_index;
  int size;
  int capacity;
} edges_t;

my_error_t allocate_edges(edges_t *edges);
void free_edges(edges_t *edges);
void edges_default(edges_t *edges);
my_error_t save_all_edges(const edges_t *edges, FILE *fout);
my_error_t save_edge(const edge_t *edge, FILE *fout);
my_error_t append_edge(edges_t *edges, edge_t edge);

#ifdef __cplusplus
}
#endif

#endif  // EDGES_H
