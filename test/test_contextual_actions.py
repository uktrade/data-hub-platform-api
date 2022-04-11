class GetContextualActions:
    def __call__(self):
        return {
            'actions': []
        }


def test_can_get_no_contextual_actions():
    get_contextual_actions = GetContextualActions()
    response = get_contextual_actions()
    buttons = response['actions']
    assert [] == buttons
