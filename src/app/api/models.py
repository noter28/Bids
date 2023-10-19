from pydantic import BaseModel


# class NoteSchema(BaseModel):
#     name: str
#     identification_number: str
#     delivery_start_date: str
#     delivery_end_date: str
#     distribution_system_operator: str
#     ordered_volumes_first_voltage_class_a: str
#     ordered_volumes_first_voltage_class_b: str
#     ordered_volumes_second_voltage_class_a: str
#     ordered_volumes_second_voltage_class_b: str
#     ordered_volumes_by_voltage_first_class: str
#     ordered_volumes_by_voltage_second_class: str
#     ordered_volumes_a: str
#     ordered_volumes_b: str
#     total: str
#     created_date: str

class NoteSchema(BaseModel):
    title: str
    description: str


class NoteDB(NoteSchema):
    id: int
