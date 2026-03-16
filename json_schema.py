class SchemaValidator:
    def validate(s, data, schema):
        errors = []; s._validate(data, schema, "", errors); return errors
    def _validate(s, data, schema, path, errors):
        t = schema.get("type")
        if t == "string" and not isinstance(data, str): errors.append(f"{path}: expected string")
        elif t == "integer" and not isinstance(data, int): errors.append(f"{path}: expected integer")
        elif t == "number" and not isinstance(data, (int, float)): errors.append(f"{path}: expected number")
        elif t == "boolean" and not isinstance(data, bool): errors.append(f"{path}: expected boolean")
        elif t == "array":
            if not isinstance(data, list): errors.append(f"{path}: expected array"); return
            items = schema.get("items")
            if items:
                for i, item in enumerate(data): s._validate(item, items, f"{path}[{i}]", errors)
            mn, mx = schema.get("minItems"), schema.get("maxItems")
            if mn and len(data) < mn: errors.append(f"{path}: minItems {mn}")
            if mx and len(data) > mx: errors.append(f"{path}: maxItems {mx}")
        elif t == "object":
            if not isinstance(data, dict): errors.append(f"{path}: expected object"); return
            props = schema.get("properties", {})
            for k, v in props.items():
                if k in data: s._validate(data[k], v, f"{path}.{k}", errors)
            for req in schema.get("required", []):
                if req not in data: errors.append(f"{path}.{req}: required")
        if "enum" in schema and data not in schema["enum"]:
            errors.append(f"{path}: must be one of {schema['enum']}")
        mn, mx = schema.get("minimum"), schema.get("maximum")
        if mn is not None and isinstance(data, (int,float)) and data < mn: errors.append(f"{path}: minimum {mn}")
        if mx is not None and isinstance(data, (int,float)) and data > mx: errors.append(f"{path}: maximum {mx}")
def demo():
    schema = {"type":"object","required":["name","age"],"properties":{
        "name":{"type":"string"},"age":{"type":"integer","minimum":0,"maximum":150},
        "tags":{"type":"array","items":{"type":"string"},"maxItems":5}}}
    v = SchemaValidator()
    tests = [{"name":"Alice","age":30,"tags":["admin"]}, {"name":123,"age":-1}, {"age":30}, {"name":"X","age":200}]
    for data in tests:
        errs = v.validate(data, schema)
        print(f"  {str(data):45s} -> {'OK' if not errs else errs}")
if __name__ == "__main__": demo()
