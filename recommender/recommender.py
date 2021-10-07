from . import CATEGORIES, TEST_MESSAGES
from scipy.stats import beta


class Recommender:
    """
    Class in charge of multi-armed bandit recommendations.
    See: https://en.wikipedia.org/wiki/Multi-armed_bandit
    """

    def __init__(self):
        """
        Setting up consumer and user profiles.
        """
        self.consumer = None
        self.user_profiles = {}

    def run(self):
        """
        Run the recommender.
        """
        it = 0
        while it<100:
            self._process(TEST_MESSAGES)
            it +=1

    def _ingest_kafka(self):
        """
        Ingest Kafka messages by batches.
        """
        return self.consumer.consume(num_messages=2, timeout=1)

    def _init_arms(self, session_id):
        """
        Initialisation of arms (categories) with beta distributions parameters.
        :param str session_id: the session ID of the user to recommend for.
        """
        self.user_profiles[session_id] = {}
        for category in CATEGORIES:
            self.user_profiles[session_id][category] = (2, 2)

    def _process(self, messages):
        """
        Consuming a batch of messages ingested.
        :param list messages: a list of messages to process.
        """
        for message in messages:
            category = self._get_category(message)
            session_id = self._get_session_id(message)
            reward = self._get_reward(message)
            try:
                self._update_arm(session_id, category, reward)
            except KeyError:
                self._init_arms(session_id)
            print(self._get_recommendations(session_id))

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
        :param dict message: the message received from mparticles.
        :return str category: the category of the message.
        """
        return message["data"]["product_action"]["products"][0]["category"]

    def _get_session_id(self, message):
        """
        Getting the session ID of the user.
        :param dict message: the message received from mparticles.
        :return str category: the session ID of the message.
        """
        return message["session_id"]

    def _update_arm(self, session_id, category, reward):
        """
        Updating arm based on reward received.
        :param str session_id: the session ID.
        :param str category: the category of the message.
        :param float reward: the reward associated with the action.
        """
        self.user_profiles[session_id][category] = (
            self.user_profiles[session_id][category][0] + reward,
            self.user_profiles[session_id][category][1] + (1 - reward))

    def _get_recommendations(self, session_id, top=5):
        """
        Getting the recommendations based on Thomson Sampling (TS).
        i.e: we generate random values for each category and pick the top ones.
        :param str session_id: the session ID of the user to recommend for.
        :param int top: the number of recommendations we want (e.g: top 5)
        :return list recommendations: list of top categories based on TS.
        """

        categories = list(self.user_profiles[session_id].items())
        categories.sort(
            key=lambda category: beta.rvs(
                category[1][0], category[1][1], size=1)[0],
            reverse=True)
        return [category[0] for category in categories[:top]]
