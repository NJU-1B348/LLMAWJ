# Prompt Test-cases

## Never Free Cases

```json
// Test case 1
{
    "DefectType": "Never Free",
    "Location": {
        "ln": 358,
        "cl": 12,
        "fl": "httpd-2.4.23/server/util_script.c"
    },
    "Function": "original_uri",
    "Description": {},
    "Events": [],
    "Var": [
        "first"
    ],
    "CodeNear": [
        "first = r->the_request;     /* use the request-line */",
        "",
        "while (*first && !apr_isspace(*first)) {",
        "++first;                /* skip over the method */",
        "}",
        "while (apr_isspace(*first)) {",
        "++first;                /*   and the space(s)   */",
        "}",
        "",
        "last = first;",
        "while (*last && !apr_isspace(*last)) {"
    ],
    "SuccessTransform": "True",
    "TransformMessage": ""
}
// False

// Test case 2
{
    "DefectType": "Never Free",
    "Location": {
        "ln": 1380,
        "cl": 31,
        "fl": "util.c"
    },
    "Function": "find_list_item",
    "Description": {},
    "Events": [],
    "Var": [
        "ptr"
    ],
    "CodeNear": [
        "}",
        "",
        "do {  /* loop for each item in line's list */",
        "",
        "/* Find first non-comma, non-whitespace byte */",
        "while (*ptr == ',' || apr_isspace(*ptr)) {",
        "++ptr;",
        "}",
        "",
        "/* Account for strong or weak Etags, depending on our search */",
        "if (type == AP_ETAG_STRONG && *ptr != '\\\"') {"
    ],
    "SuccessTransform": "True",
    "TransformMessage": ""
}
// False

// Test case 3
{
    "DefectType": "Never Free",
    "Location": {
        "ln": 871,
        "cl": 12,
        "fl": "util.c"
    },
    "Function": "ap_getword_conf2",
    "Description": {},
    "Events": [],
    "Var": [
        "strend"
    ],
    "CodeNear": [
        "++strend;",
        "",
        "res = substring_conf(p, str, strend - str, 0);",
        "}",
        "",
        "while (apr_isspace(*strend))",
        "++strend;",
        "*line = strend;",
        "return res;",
        "}",
        ""
    ],
    "SuccessTransform": "True",
    "TransformMessage": ""
}
// False

// Test case 4
{
    "DefectType": "Never Free",
    "Location": {
        "ln": 355,
        "cl": 23,
        "fl": "httpd-2.4.23/server/util_script.c"
    },
    "Function": "original_uri",
    "Description": {},
    "Events": [],
    "Var": [
        "first"
    ],
    "CodeNear": [
        "return (char *) apr_pcalloc(r->pool, 1);",
        "}",
        "",
        "first = r->the_request;     /* use the request-line */",
        "",
        "while (*first && !apr_isspace(*first)) {",
        "++first;                /* skip over the method */",
        "}",
        "while (apr_isspace(*first)) {",
        "++first;                /*   and the space(s)   */",
        "}"
    ],
    "SuccessTransform": "True",
    "TransformMessage": ""
}
// False

// Test case 5
{
    "DefectType": "Never Free",
    "Location": {
        "ln": 1019,
        "cl": 9,
        "fl": "httpd-2.4.23/server/mpm_unix.c"
    },
    "Function": "ap_fatal_signal_setup",
    "Description": {},
    "Events": [],
    "Var": [
        "errno",
        "s"
    ],
    "CodeNear": [
        "sa.sa_handler = sig_coredump;",
        "if (sigaction(SIGSEGV, &sa, NULL) < 0)",
        "ap_log_error(APLOG_MARK, APLOG_WARNING, errno, s, APLOGNO(00061) \"sigaction(SIGSEGV)\");",
        "#ifdef SIGBUS",
        "if (sigaction(SIGBUS, &sa, NULL) < 0)",
        "ap_log_error(APLOG_MARK, APLOG_WARNING, errno, s, APLOGNO(00062) \"sigaction(SIGBUS)\");",
        "#endif",
        "#ifdef SIGABORT",
        "if (sigaction(SIGABORT, &sa, NULL) < 0)",
        "ap_log_error(APLOG_MARK, APLOG_WARNING, errno, s, APLOGNO(00063) \"sigaction(SIGABORT)\");",
        "#endif"
    ],
    "SuccessTransform": "True",
    "TransformMessage": ""
}
// False

// Test case 6
{
    "DefectType": "Never Free",
    "Location": {
        "ln": 206,
        "cl": 30,
        "fl": "httpd-2.4.23/modules/http/http_filters.c"
    },
    "Function": "parse_chunk_size",
    "Description": {},
    "Events": [],
    "Var": [
        "c"
    ],
    "CodeNear": [
        "}",
        "else if (ctx->state == BODY_CHUNK_EXT) {",
        "/*",
        "* Control chars (but tabs) are invalid.",
        "*/",
        "if (c != '\\t' && apr_iscntrl(c)) {",
        "return APR_EINVAL;",
        "}",
        "}",
        "else if (c == ' ' || c == '\\t') {",
        "/* Be lenient up to 10 BWS (term from rfc7230 - 3.2.3)."
    ],
    "SuccessTransform": "True",
    "TransformMessage": ""
}
// False

// Test Case 7
{
    "DefectType": "Never Free",
    "Location": {
        "ln": 28,
        "cl": 20,
        "fl": "malloc4.c"
    },
    "Function": "foo",
    "Description": {},
    "Events": [],
    "Var": [
        "q"
    ],
    "CodeNear": [
        "int bar(int* s){",
        "	free(s);",
        "}",
        "",
        "int foo(network_t* net){",
        "	int *p = MACROMALLOC(10);",
        "	int *q = MACROMALLOC(10);",
        "	net->arcs = p;",
        "	net->stop = q;",
        "	bar(net->arcs);",
        ""
    ],
    "SuccessTransform": "True",
    "TransformMessage": ""
}
// True

// Test Case 8
{
    "DefectType": "Never Free",
    "Location": {
        "ln": 27,
        "cl": 5,
        "fl": "malloc9.c"
    },
    "Function": "main",
    "Description": {},
    "Events": [],
    "Var": [
        "rr_node[i].edges"
    ],
    "CodeNear": [
        "	return MACROMALLOC(10);",
        "}",
        "",
        "int main(){",
        "	//rr_node = malloc(sizeof(struct s_rr_node)*10);",
        "	int i;",
        "	rr_node[i].edges = alloc();",
        "",
        "	//free(rr_node[i].edges);",
        "",
        "}"
    ],
    "SuccessTransform": "True",
    "TransformMessage": ""
}
// True

// Test Case 9
{
    "DefectType": "Never Free",
    "Location": {
        "ln": 28,
        "cl": 20,
        "fl": "malloc10.c"
    },
    "Function": "main",
    "Description": {},
    "Events": [],
    "Var": [
        "rr_node[i][i].edges"
    ],
    "CodeNear": [
        "",
        "int main(){",
        "struct s_rr_node **rr_node;",
        "	rr_node = MACROMALLOC(sizeof(struct s_rr_node)*10);",
        "	int i;",
        "	rr_node[i][i].edges = MACROMALLOC(10);",
        "	free(rr_node);",
        "	printf(\"%d\",rr_node);",
        "}"
    ],
    "SuccessTransform": "True",
    "TransformMessage": ""
}
// True

// Test Case 10
{
    "DefectType": "Never Free",
    "Location": {
        "ln": 27,
        "cl": 5,
        "fl": "malloc21.c"
    },
    "Function": "readmin",
    "Description": {},
    "Events": [],
    "Var": [
        "net1.f1"
    ],
    "CodeNear": [
        "	free(net->f2);",
        "	free(net->f3);",
        "}",
        "",
        "void readmin(){",
        "	FOO net1;",
        "	net1.f1 = (int*)MACROMALLOC(sizeof(int));",
        "	net1.f2 = (int*)MACROMALLOC(2);",
        "	net1.f3 = (int*)MACROMALLOC(3);",
        "	printf(\"%d,%d,%d\",net1.f1,net1.f2,net1.f3);",
        "",
        "}",
        ""
    ],
    "SuccessTransform": "True",
    "TransformMessage": ""
}
// True

// Test Case 11
{
    "DefectType": "Never Free",
    "Location": {
        "ln": 11,
        "cl": 5,
        "fl": "malloc23.c"
    },
    "Function": "func",
    "Description": {},
    "Events": [],
    "Var": [
        "p"
    ],
    "CodeNear": [
        "",
        "#include \"memleak_check.h\"",
        "",
        "int func(){",
        "",
        "	int* p = MACROMALLOC(1);",
        "",
        "	free(p);",
        "",
        "	int *q = MACROMALLOC(1);",
        ""
    ],
    "SuccessTransform": "True",
    "TransformMessage": ""
}
// False

// Test Case 12
{
    "DefectType": "Never Free",
    "Location": {
        "ln": 12,
        "cl": 5,
        "fl": "malloc25.c"
    },
    "Function": "func",
    "Description": {},
    "Events": [],
    "Var": [
        "atms"
    ],
    "CodeNear": [
        "",
        "#include \"memleak_check.h\"",
        "",
        "int func(){",
        "	int i;",
        "	int* atms = MACROMALLOC(10);",
        "",
        "	if(atms==0)",
        "		return 0;",
        "",
        ""
    ],
    "SuccessTransform": "True",
    "TransformMessage": ""
}
//True

// Test Case 13
{
    "DefectType": "Never Free",
    "Location": {
        "ln": 12,
        "cl": 5,
        "fl": "malloc14.c"
    },
    "Function": "func",
    "Description": {},
    "Events": [],
    "Var": [
        "p"
    ],
    "CodeNear": [
        "",
        "int main(){",
        "",
        "",
        "	int *p = MACROMALLOC(1);",
        "	int i,*q;",
        "	q = p + i;",
        "	printf(\"%d%d\",p,q);",
        "}"
    ],
    "SuccessTransform": "True",
    "TransformMessage": ""
}
// True
```