HXCOMM Use DEFHEADING() to define headings in both help text and texi
HXCOMM Text between STEXI and ETEXI are copied to texi version and
HXCOMM discarded from C version
HXCOMM DEF(command, args, callback, arg_string, help) is used to construct
HXCOMM monitor info commands
HXCOMM HXCOMM can be used for comments, discarded from both texi and C

STEXI
@table @option
@item virtio  @var{subcommand}
@findex virtio
Show various information about virtio
@table @option
ETEXI

    {
        .name       = "query",
        .args_type  = "",
        .params     = "",
        .help       = "List all available virtio devices",
        .cmd        = hmp_virtio_query,
        .flags      = "p",
    },

STEXI
@item virtio query
@findex virtio query
List all available virtio devices
ETEXI

    {
        .name       = "status",
        .args_type  = "path:s",
        .params     = "path",
        .help       = "Display status of a given virtio device",
        .cmd        = hmp_virtio_status,
        .flags      = "p",
    },

STEXI
@item virtio status
@findex virtio status
Display status of a given virtio device
ETEXI

    {
        .name       = "queue-status",
        .args_type  = "path:s,queue:i",
        .params     = "path queue",
        .help       = "Display status of a given virtio queue",
        .cmd        = hmp_virtio_queue_status,
        .flags      = "p",
    },

STEXI
@item virtio queue-status
@findex virtio queue-status
Display status of a given virtio queue
ETEXI

    {
        .name       = "queue-element",
        .args_type  = "path:s,queue:i,index:i?",
        .params     = "path queue [index]",
        .help       = "Display element of a given virtio queue",
        .cmd        = hmp_virtio_queue_element,
        .flags      = "p",
    },

STEXI
@item virtio queue-element
@findex virtio queue-element
Display element of a given virtio queue
ETEXI

STEXI
@end table
ETEXI

STEXI
@end table
ETEXI
