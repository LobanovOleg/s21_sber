#include "edges.h"

my_error_t allocate_edges(edges_t* edges) {
  my_error_t rc = SUCCESS;
  if (edges->size <= 0)
    rc = SIZE_EDGES_ERROR;
  else {
    edge_t* temp_array = (edge_t*)malloc(edges->size * sizeof(edge_t));
    if (!temp_array)
      rc = MEMORY_ALLOCATE_ERROR;
    else
      edges->array_edges = temp_array;
  }
  return rc;
}

void edges_default(edges_t* edges) {
  edges->array_edges = NULL;
  edges->last_index = -1;
  edges->size = 0;
  edges->capacity = 0;
}

void free_edges(edges_t* edges) {
  if (edges) {
    free(edges->array_edges);
    edges_default(edges);
  }
}

my_error_t save_all_edges(const edges_t* edges, FILE* fout) {
  my_error_t rc = SUCCESS;
  for (int i = 0; rc == SUCCESS && i < edges->size; i++)
    rc = save_edge(&edges->array_edges[i], fout);

  return rc;
}

my_error_t save_edge(const edge_t* edge, FILE* fout) {
  int rc = fprintf(fout, "l %d %d\n", edge->first_point, edge->second_point);
  if (0 > rc) return FILE_WRITE_ERROR;
  return SUCCESS;
}

void* my_edges_realloc(edges_t* edges, int new_size) {
  if (new_size > edges->capacity) {
    int new_capacity = (edges->capacity == 0) ? 1 : edges->capacity * 2;
    while (new_size > new_capacity) {
      new_capacity *= 2;
    }
    if (edges->array_edges == NULL)
      edges->array_edges = (edge_t*)malloc(new_capacity * sizeof(edge_t));
    else
      edges->array_edges =
          (edge_t*)realloc(edges->array_edges, new_capacity * sizeof(edge_t));
    edges->capacity = new_capacity;
  }

  return edges->array_edges;
}

my_error_t append_edge(edges_t* edges, edge_t edge) {
  int rc = SUCCESS;
  if (edges->size == edges->capacity) {
    edges->array_edges = (edge_t*)my_edges_realloc(edges, edges->size + 1);
    if (!edges->array_edges) rc = MEMORY_ALLOCATE_ERROR;
  }
  if (!rc) {
    edges->array_edges[edges->size] = edge;
    edges->size++;
  }
  return rc;
}
