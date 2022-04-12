class DescribeActionContext:
    def __init__(self, action_context_gateway):
        self.action_context_gateway = action_context_gateway

    def __call__(self, context_id):
        return {
            'object': {
                'id': context_id
            },
            'success': True
        }
