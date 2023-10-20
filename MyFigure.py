from pyscratch.figure import Figure


class MyFigure(Figure):
    def __init__(self):
        super().__init__("ball.png")

    def on_key_up_w(self):
        print("Scaling")
        self.scale(2)
