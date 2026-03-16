#!/usr/bin/env python3
"""JSON Schema validator (draft-07 subset)."""
import json, sys, re

def validate(instance, schema, path="$"):
    errors=[]
    if "type" in schema:
        type_map={"string":str,"number":(int,float),"integer":int,"boolean":bool,"array":list,"object":dict,"null":type(None)}
        expected=type_map.get(schema["type"])
        if expected and not isinstance(instance,expected):
            errors.append(f"{path}: expected {schema['type']}, got {type(instance).__name__}")
            return errors
    if isinstance(instance,dict) and "properties" in schema:
        for prop,sub in schema["properties"].items():
            if prop in instance: errors.extend(validate(instance[prop],sub,f"{path}.{prop}"))
        if "required" in schema:
            for req in schema["required"]:
                if req not in instance: errors.append(f"{path}: missing required '{req}'")
    if isinstance(instance,list) and "items" in schema:
        for i,item in enumerate(instance):
            errors.extend(validate(item,schema["items"],f"{path}[{i}]"))
    if isinstance(instance,str):
        if "minLength" in schema and len(instance)<schema["minLength"]:
            errors.append(f"{path}: too short (min {schema['minLength']})")
        if "pattern" in schema and not re.search(schema["pattern"],instance):
            errors.append(f"{path}: pattern mismatch")
    if isinstance(instance,(int,float)):
        if "minimum" in schema and instance<schema["minimum"]:
            errors.append(f"{path}: below minimum {schema['minimum']}")
        if "maximum" in schema and instance>schema["maximum"]:
            errors.append(f"{path}: above maximum {schema['maximum']}")
    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: not in enum {schema['enum']}")
    return errors

if __name__ == "__main__":
    schema={"type":"object","required":["name","age"],
            "properties":{"name":{"type":"string","minLength":1},
                          "age":{"type":"integer","minimum":0,"maximum":150},
                          "email":{"type":"string","pattern":r"@"}}}
    valid={"name":"Alice","age":30,"email":"a@b.com"}
    invalid={"name":"","age":-5,"email":"nope"}
    missing={"name":"Bob"}
    for label,data in [("valid",valid),("invalid",invalid),("missing",missing)]:
        errs=validate(data,schema)
        print(f"  {label}: {'✅ valid' if not errs else '❌ '+'; '.join(errs)}")
