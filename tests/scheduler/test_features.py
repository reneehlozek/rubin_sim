import os
import numpy as np
import unittest
import rubin_sim.scheduler.features as features
from rubin_sim.scheduler.utils import empty_observation
from rubin_sim.scheduler.model_observatory import Model_observatory
from rubin_sim.data import get_data_dir


class TestFeatures(unittest.TestCase):
    def testPair_in_night(self):
        pin = features.Pair_in_night(gap_min=25.0, gap_max=45.0)
        self.assertEqual(np.max(pin.feature), 0.0)

        indx = np.array([1000])

        delta = 30.0 / 60.0 / 24.0

        # Add 1st observation, feature should still be zero
        obs = empty_observation()
        obs["filter"] = "r"
        obs["mjd"] = 59000.0
        pin.add_observation(obs, indx=indx)
        self.assertEqual(np.max(pin.feature), 0.0)

        # Add 2nd observation
        obs["mjd"] += delta
        pin.add_observation(obs, indx=indx)
        self.assertEqual(np.max(pin.feature), 1.0)

        obs["mjd"] += delta
        pin.add_observation(obs, indx=indx)
        self.assertEqual(np.max(pin.feature), 2.0)

    def testConditions(self):
        observatory = Model_observatory(
            seeing_db=os.path.join(get_data_dir(), "tests", "seeing.db"),
        )
        conditions = observatory.return_conditions()
        self.assertIsInstance(repr(conditions), str)
        self.assertIsInstance(str(conditions), str)

    def test_note_last_observed(self):

        note_last_observed = features.NoteLastObserved(note="test")

        observation = empty_observation()
        observation["mjd"] = 59000.0

        note_last_observed.add_observation(observation=observation)

        assert note_last_observed.feature is None

        observation["note"] = "foo"

        note_last_observed.add_observation(observation=observation)
        assert note_last_observed.feature is None

        observation["note"] = "test"

        note_last_observed.add_observation(observation=observation)
        assert note_last_observed.feature == observation["mjd"]

    def test_note_last_observed_with_filter(self):

        note_last_observed = features.NoteLastObserved(
            note="test",
            filtername="r",
        )

        observation = empty_observation()
        observation["mjd"] = 59000.0

        note_last_observed.add_observation(observation=observation)

        assert note_last_observed.feature is None

        observation["note"] = "foo"

        note_last_observed.add_observation(observation=observation)
        assert note_last_observed.feature is None

        observation["note"] = "test"
        observation["filter"] = "g"

        note_last_observed.add_observation(observation=observation)
        assert note_last_observed.feature is None

        observation["note"] = "test"
        observation["filter"] = "r"

        note_last_observed.add_observation(observation=observation)
        assert note_last_observed.feature == observation["mjd"]


if __name__ == "__main__":
    unittest.main()
