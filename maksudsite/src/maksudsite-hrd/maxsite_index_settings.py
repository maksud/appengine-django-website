from maxsite.models import Conference

FIELD_INDEXES = {
    Conference: {'indexed': ['long_name']}
}