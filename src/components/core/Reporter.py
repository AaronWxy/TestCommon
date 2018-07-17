import os
from pyhtml import *
from src.resource.style import css


class Report(object):

    def __init__(self, metadata, runner, path="Output/report.html"):

        if not os.path.isfile(path):
            with open(path, 'a'):
                pass 
        
        t = html(
                head(
                    title('Automation Test Result'),
                    meta(charset="utf-8"),
                    meta(name="viewport", content="width=device-width, initial-scale=1"),
                    style(css)
                ),
                body(
                    div(class=container),
                    div(class=panel),
                    div(class=panel-footer, self.record_metadata)
                    div(class=panel-body,
                        table(
                            tr(
                                th('TEST #'),
                                th('TEST CASE'),
                                th('START TIME'),
                                th('DURATION'),
                                th('RESULT'),
                                th('LOG')
                            ),
                            self.record_results
                        )
                    )
                )
            )

        self.html = t
        self.html_file = path
    
    def record_metadata(self, metadata):
        pass 

    def record_results(self, result_collection):
        pass 

    def finalized_report(self):

        with open(self.html_file, 'a+') as f:
            print "AAA"
            print self.html.render()
        f.write(self.html.render())



