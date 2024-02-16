from topicaxisapi.database.models import Category
from topicaxisapi.mappers.base import Mapper
from topicaxisapi.models import Category as CategoryDomain


class CategoryDatabaseToDomainMapper(Mapper[Category, CategoryDomain]):
    def map(self, item: Category) -> CategoryDomain:
        return CategoryDomain(
            id=item.id, name=item.name, taxonomy=item.taxonomy
        )
