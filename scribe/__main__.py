"""
The main program module for this application.
"""
import logging
from scribe.app.context import AppContext
from scribe.app.cli.arguments import AppMode
from scribe.generator import GenerateService
from scribe.uploader import UploadService

class Program:
    """
    The main program class for this application.
    """

    @staticmethod
    def main() -> None:
        """
        Main entry point for this application.
        """
        app:AppContext = AppContext.create()
        if app.arguments.mode == AppMode.GENERATE:
            _ = GenerateService.start(app)
        elif app.arguments.mode == AppMode.UPLOAD:
            _ = UploadService.start(app)
        else:
            logging.error(f"Unknown argument for 'mode': {app.arguments.mode}")


# Main
#---------------------------------------------

if __name__ == "__main__":
    Program.main()
