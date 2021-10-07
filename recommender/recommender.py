from . import CATEGORIES
from scipy.stats import beta


class Recommender:

    def __init__(self):
        self.consumer = None
        self.user_profiles = {}

    def run(self):
        it = 0
        while it<100:
            it +=1
            messages = [{
                "data": {
                    "product_action": {
                        "action": "add_to_cart",
                        "products": [{
                            "id": "P10000",
                            "name": "Black skirt",
                            "brand": "N/A",
                            "category": "skirts",
                            "price": 16.0,
                            "quantity": 1.0,
                            "total_product_amount": 16.0
                        }]
                    },
                },
                "session_id": "11223344",
            }]
            self._process(messages)

    def _ingest_kafka(self):
        """
        The user can control the size of the batch and the timeout from the
        configuration file.
        """
        return self.consumer.consume(num_messages=2, timeout=1)

    def _init_arms(self, session_id):
        """
        Initialisation of arms (categories) with beta distributions parameters.
        """
        self.user_profiles[session_id] = {}
        for category in CATEGORIES:
            self.user_profiles[session_id][category] = (2, 2)

    def _process(self, messages):
        """
        Consuming a batch of messages.
        :param list messages: a list of messages ("batches") to process.
        e.g: [<kafka.cimpl_1>, <kafka.cimpl_2>, <kafka.cimpl_3>]
        """
        for message in messages:
            category = self._get_category(message)
            session_id = self._get_session_id(message)
            reward = self._get_reward(message)
            try:
                self._update_arm(session_id, category, reward)
            except KeyError:
                self._init_arms(session_id)
            return self._get_recommendations(session_id)


    def _get_reward(self, message):
        """
        Getting the action reward depending on message type.
        :param dict message: the message received from mparticles.
        :return float reward: the reward attached to the type of action.
        """
        reward = 0
        if message["data"]["product_action"]["action"] == "add_to_cart":
            reward = 1
        return reward

    def _get_category(self, message):
        """
        Getting the category of the product ingested.
        :param message:
        :return:
        """
        return message["data"]["product_action"]["products"][0]["category"]

    def _get_session_id(self, message):
        """
        Getting the session ID of the user.
        :param message:
        :return:
        """
        return message["session_id"]

    def _update_arm(self, session_id, category, reward):
        self.user_profiles[session_id][category] = (
            self.user_profiles[session_id][category][0] + reward,
            self.user_profiles[session_id][category][1] + (1 - reward))

    def _get_recommendations(self, session_id, top=5):
        """
        Getting the recommendations based on Thomson Sampling (TS).
        i.e: we generate random values for each category and pick the top ones.
        :return list recommendations: list of top categories based on TS.
        """

        top_categories = list(self.user_profiles[session_id].items())
        top_categories.sort(
            key=lambda category: beta.rvs(
                category[1][0], category[1][1], size=1)[0],
            reverse=True)
        return [category[0] for category in top_categories[:top]]
