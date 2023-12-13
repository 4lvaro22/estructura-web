from models.entity_dto import Entity, EntityForm

def entityEntity(entity) -> Entity:
    return Entity(**{
        **entity,
        "id": str(entity["_id"])})


def entityList(entities) -> list[Entity]:
    return [entityEntity(entity) for entity in entities]

def entityEntityForm(entity):
    return EntityForm({**entity})