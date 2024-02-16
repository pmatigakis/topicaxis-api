from topicaxisapi.exceptions import TopicaxisApiError


class TopicaxisApiRouterError(TopicaxisApiError):
    pass


class ArticleSearchError(TopicaxisApiRouterError):
    pass
