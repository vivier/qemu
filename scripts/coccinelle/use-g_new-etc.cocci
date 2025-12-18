// Use g_new() & friends where that makes obvious sense

@r@
type T;
identifier S, f;
@@
struct S {
  ...
  T *f;
  ...
};

// n = 1, size = sizeof(T)

// g_malloc()
@@
type T;
@@
-g_malloc(sizeof(T))
+g_new(T, 1)

@@
type T;
T *E;
@@
-g_malloc(sizeof(*E))
+g_new(T, 1)

@@
type r.T;
identifier r.f;
expression s;
@@
-g_malloc(sizeof(*s->f))
+g_new(T, 1)

// g_try_malloc()
@@
type T;
@@
-g_try_malloc(sizeof(T))
+g_try_new(T, 1)

@@
type T;
T *E;
@@
-g_try_malloc(sizeof(*E))
+g_try_new(T, 1)

@@
type r.T;
identifier r.f;
expression s;
@@
-g_try_malloc(sizeof(*s->f))
+g_try_new(T, 1)

// g_malloc0()
@@
type T;
@@
-g_malloc0(sizeof(T))
+g_new0(T, 1)

@@
type T;
T *E;
@@
-g_malloc0(sizeof(*E))
+g_new0(T, 1)

@@
type r.T;
identifier r.f;
expression s;
@@
-g_malloc0(sizeof(*s->f))
+g_new0(T, 1)

// g_try_malloc0()
@@
type T;
@@
-g_try_malloc0(sizeof(T))
+g_try_new0(T, 1)

@@
type T;
T *E;
@@
-g_try_malloc0(sizeof(*E))
+g_try_new0(T, 1)

@@
type r.T;
identifier r.f;
expression s;
@@
-g_try_malloc0(sizeof(*s->f))
+g_try_new0(T, 1)

// n=n, size = sizeof(T)

// g_malloc()
@@
type T;
expression n;
@@
-g_malloc(sizeof(T) * (n))
+g_new(T, n)

@@
type T;
T *E;
expression n;
@@
-g_malloc(sizeof(*E) * (n))
+g_new(T, n)

@@
type r.T;
identifier r.f;
expression s, n;
@@
-g_malloc(sizeof(*s->f) * (n))
+g_new(T, n)

// g_malloc_n()
@@
type T;
expression n;
@@
-g_malloc_n((n), sizeof(T))
+g_new(T, n)

@@
type T;
T *E;
expression n;
@@
-g_malloc_n((n), sizeof(*E))
+g_new(T, n)

@@
type r.T;
identifier r.f;
expression s, n;
@@
-g_malloc_n((n), sizeof(*s->f))
+g_new(T, n)

// g_try_malloc()
@@
type T;
expression n;
@@
-g_try_malloc(sizeof(T) * (n))
+g_try_new(T, n)

@@
type T;
T *E;
expression n;
@@
-g_try_malloc(sizeof(*E) * (n))
+g_try_new(T, n)

@@
type r.T;
identifier r.f;
expression s, n;
@@
-g_try_malloc(sizeof(*s->f) * (n))
+g_try_new(T, n)

// g_try_malloc_n()
@@
type T;
expression n;
@@
-g_try_malloc_n((n), sizeof(T))
+g_try_new(T, n)

@@
type T;
T *E;
expression n;
@@
-g_try_malloc_n((n), sizeof(*E))
+g_try_new(T, n)

@@
type r.T;
identifier r.f;
expression s, n;
@@
-g_try_malloc_n((n), sizeof(*s->f))
+g_try_new(T, n)

// g_malloc0()
@@
type T;
expression n;
@@
-g_malloc0(sizeof(T) * (n))
+g_new0(T, n)

@@
type T;
T *E;
expression n;
@@
-g_malloc0(sizeof(*E) * (n))
+g_new0(T, n)

@@
type r.T;
identifier r.f;
expression s, n;
@@
-g_malloc0(sizeof(*s->f) * (n))
+g_new0(T, n)

// g_malloc0_n()
@@
type T;
expression n;
@@
-g_malloc0_n((n), sizeof(T))
+g_new0(T, n)

@@
type T;
T *E;
expression n;
@@
-g_malloc0_n((n), sizeof(*E))
+g_new0(T, n)

@@
type r.T;
identifier r.f;
expression s, n;
@@
-g_malloc0_n((n), sizeof(*s->f))
+g_new0(T, n)

// g_try_malloc0()
@@
type T;
expression n;
@@
-g_try_malloc0(sizeof(T) * (n))
+g_try_new0(T, n)

@@
type T;
T *E;
expression n;
@@
-g_try_malloc0(sizeof(*E) * (n))
+g_try_new0(T, n)

@@
type r.T;
identifier r.f;
expression s, n;
@@
-g_try_malloc0(sizeof(*s->f) * (n))
+g_try_new0(T, n)

// g_try_malloc0_n()
@@
type T;
expression n;
@@
-g_try_malloc0_n((n), sizeof(T))
+g_try_new0(T, n)

@@
type T;
T *E;
expression n;
@@
-g_try_malloc0_n((n), sizeof(*E))
+g_try_new0(T, n)

@@
type r.T;
identifier r.f;
expression s, n;
@@
-g_try_malloc0_n((n), sizeof(*s->f))
+g_try_new0(T, n)

// g_realloc()
@@
type T;
expression p, n;
@@
-g_realloc(p, sizeof(T) * (n))
+g_renew(T, p, n)

@@
type T;
T *E;
expression p, n;
@@
-g_realloc(p, sizeof(*E) * (n))
+g_renew(T, p, n)

@@
type r.T;
identifier r.f;
expression s, p, n;
@@
-g_realloc(p, sizeof(*s->f) * (n))
+g_renew(T, p, n)

// g_try_realloc()
@@
type T;
expression p, n;
@@
-g_try_realloc(p, sizeof(T) * (n))
+g_try_renew(T, p, n)

@@
type T;
T *E;
expression p, n;
@@
-g_try_realloc(p, sizeof(*E) * (n))
+g_try_renew(T, p, n)

@@
type r.T;
identifier r.f;
expression s, p, n;
@@
-g_try_realloc(p, sizeof(*s->f) * (n))
+g_try_renew(T, p, n)

// remove casting
@@
type T;
expression n;
@@
-(T *)g_new(T, n)
+g_new(T, n)
@@
type T;
expression n;
@@
-(T *)g_new0(T, n)
+g_new0(T, n)
@@
type T;
expression p, n;
@@
-(T *)g_renew(T, p, n)
+g_renew(T, p, n)
