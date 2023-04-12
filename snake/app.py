from dash import Dash, Output, Input, State
from dash.dcc import Graph, Interval, Store
from dash.exceptions import PreventUpdate
from dash.html import Div
from dash_extensions import EventListener
from plotly.express import imshow
from snake.direction import Direction
from snake.game import Game

FRAME_RATE = 5
CONTROL_MAPPER = {
    'ArrowUp': Direction.UP,
    'ArrowDown': Direction.DOWN,
    'ArrowLeft': Direction.LEFT,
    'ArrowRight': Direction.RIGHT
}


class App(Dash):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            update_title=None,
            **kwargs
        )
        self.game = Game(10, 10)

        self.setup()

    def get_layout(self):
        return Div(
            id='app-container',
            children=[
                Interval(id='interval', interval=1_000 // FRAME_RATE),
                EventListener(
                    id='listener',
                    events=[
                        {
                            'event': 'keydown',
                            'props': ['key']
                        }
                    ]
                ),
                Store(id='store'),
                Graph(
                    id='graph',
                    figure=imshow(self.game.next())
                )
            ]
        )

    def get_callbacks(self):
        @self.callback(
            Output('store', 'data'),
            Input('interval', 'n_intervals'),
            State('graph', 'figure')
        )
        def render(_, figure):
            if self.game.is_snake_colliding_with_self():
                # game lost
                raise PreventUpdate

            # update the z-data of the figure with the next game frame
            figure['data'][0].update(dict(z=self.game.next()))

            return figure

        @self.callback(
            Output('listener', 'id'),  # callbacks need an output but this callback only updates the game state
            Input('listener', 'event')
        )
        def change_direction(event):
            if event is None:
                raise PreventUpdate

            key = event.get('key')
            direction = CONTROL_MAPPER.get(key)

            self.game.change_snake_direction(direction)

            return 'listener'

        self.clientside_callback(
            """
            function(figure) {
                return figure
            }
            """,
            Output('graph', 'figure'),
            Input('store', 'data'),
        )

    def setup(self):
        """ set up the layout and the callbacks """
        self.layout = self.get_layout()
        self.get_callbacks()


if __name__ == '__main__':
    app = App(__name__)
    app.run(debug=True)
