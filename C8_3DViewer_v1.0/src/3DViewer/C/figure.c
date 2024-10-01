#include "figure.h"

figure_t* figure_init(void) {
  static figure_t figure = {0};
  point_default(&figure.center);
  points_default(&figure.points);
  edges_default(&figure.edges);
  faces_default(&figure.faces);
  return &figure;
}

void free_figure(figure_t* figure) {
  if (figure) {
    free_faces(&figure->faces);
    free_points(&figure->points);
    free_edges(&figure->edges);
  }
}

my_error_t read_vertex(point_t* point, const char* line) {
  if (sscanf(line, "v %lf %lf %lf", &point->x, &point->y, &point->z) != 3)
    return READ_FILE_ERROR;
  return SUCCESS;
}

my_error_t read_face(face_t* face, const char* line) {
  my_error_t rc = SUCCESS;
  const char* token = strtok((char*)line, " ");
  int num_tokens = 0;
  face->size = 0;
  face->points = NULL;
  face->capacity = 0;
  while (token != NULL) {
    if (num_tokens > 0) {
      int point_index;
      if (sscanf(token, "%d", &point_index) != 1) {
        free(face->points);
        rc = READ_FILE_ERROR;
        break;
      }
      rc = append_face_point(face, point_index);
    }
    token = strtok(NULL, " ");
    num_tokens++;
  }
  if (!num_tokens) {
    free(face->points);
    rc = READ_FILE_ERROR;
  }
  return rc;
}

void fill_points_table(figure_t* figure) {
  for (int i = 0; i < figure->edges.size; ++i) {
    figure->points.points_table[figure->edges.array_edges[i].first_point]
                               [figure->edges.array_edges[i].second_point] = 1;
    figure->points.points_table[figure->edges.array_edges[i].first_point]
                               [figure->edges.array_edges[i].second_point] = 1;
  }
}

my_error_t fread_figure(figure_t* figure, FILE* fin) {
  if (fin == NULL) return FILE_OPEN_ERROR;
  *figure = *figure_init();
  my_error_t rc = SUCCESS;
  char line[256];
  while (fgets(line, sizeof(line), fin)) {
    if (strncmp(line, "v ", 2) == 0) {
      point_t vertex;
      rc = read_vertex(&vertex, line);
      if (rc) break;
      rc = append_point(&figure->points, vertex);
      if (rc) break;
    } else if (strncmp(line, "f ", 2) == 0) {
      face_t face;
      rc = read_face(&face, line);
      if (rc) break;
      rc = append_face(&figure->faces, face);
    }
  }
  if (rc)
    free_figure(figure);
  else {
    figure->points.points_table =
        (int**)calloc(figure->points.size, sizeof(int*));
    if (figure->points.points_table == NULL) {
      free_figure(figure);
      rc = MEMORY_ALLOCATE_ERROR;
    } else {
      for (int i = 0; i < figure->points.size; i++) {
        figure->points.points_table[i] =
            (int*)calloc(figure->points.size, sizeof(int));
        if (figure->points.points_table[i] == NULL) {
          rc = MEMORY_ALLOCATE_ERROR;
          free_figure(figure);
          break;
        }
      }
    }
    fill_points_table(figure);
    for (int i = 0; i < figure->faces.size; ++i) {
      rc = face_to_edges(&figure->faces.array_faces[i], &figure->edges,
                         figure->points.points_table);
      if (rc) break;
    }
  }

  if (figure->faces.size == 0 || figure->points.size == 0)
    rc = FILE_EMPTY_ERROR;

  return rc;
}

my_error_t download_figure(figure_t* figure, const char* filename) {
  if (filename == NULL) return FILE_OPEN_ERROR;

  my_error_t rc = SUCCESS;
  FILE* fin = fopen(filename, "r");
  if (fin == NULL)
    return FILE_EMPTY_ERROR;
  else {
    figure_t current_figure;
    rc = fread_figure(&current_figure, fin);
    fclose(fin);
    if (rc == SUCCESS) {
      free_figure(figure);
      *figure = current_figure;
    }
  }
  return rc;
}

my_error_t move_figure(figure_t* figure, const move_t* move) {
  move_point(&figure->center, move);
  my_error_t rc = move_all_points(&figure->points, move);
  double value = (move->dz > 0.0) ? (move->dz + 1) : (-1 / (move->dz - 1));
  scale_t scale = {value, value, value};
  return rc ? rc : scale_figure(figure, &scale);
}

my_error_t scale_figure(figure_t* figure, const scale_t* scale) {
  return scale_all_points(&figure->points, &figure->center, scale);
}

my_error_t rotate_figure(figure_t* figure, const rotate_t* rotate) {
  return rotate_all_points(&figure->points, &figure->center, rotate);
}

my_error_t save_figure(const figure_t* figure, const char* filename) {
  my_error_t rc = SUCCESS;
  if (filename == NULL)
    rc = FILE_WRITE_ERROR;
  else if (!figure->points.size || (!figure->edges.size && !figure->faces.size))
    rc = NOT_DATA_WRITE_ERROR;
  else {
    FILE* fout = fopen(filename, "w");
    if (fout == NULL)
      rc = FILE_WRITE_ERROR;
    else {
      rc = save_all_points(&figure->points, fout);
      if (rc == SUCCESS) rc = save_all_edges(&figure->edges, fout);
      if (rc == SUCCESS) rc = save_all_faces(&figure->faces, fout);
      fclose(fout);
    }
  }
  return rc;
}

my_error_t face_to_edges(const face_t* face, edges_t* edges,
                         int** points_table) {
  my_error_t rc = SUCCESS;
  for (int i = 0; i < face->size && !rc; i++) {
    edge_t edge;
    edge.first_point = face->points[(i - 1) < 0 ? face->size - 1 : (i - 1)] - 1;
    edge.second_point = face->points[i] - 1;
    if (!exist_edge(&edge, points_table)) {
      rc = append_edge(edges, edge);
      if (rc) break;
    }
  }
  return rc;
}

int exist_edge(const edge_t* edge, int** points_table) {
  return points_table[edge->first_point][edge->second_point] ||
         points_table[edge->second_point][edge->first_point];
}
