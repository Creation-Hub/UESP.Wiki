import logging
from scribe.app.context import AppContext
from scribe.app.cli import AppMode
import scribe.bot.generator
import scribe.bot.uploader


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

        if not app.arguments:
            logging.error("No command line arguments provided.")
            return

        if app.arguments.mode == AppMode.GENERATE:
            scribe.bot.generator.start(app)
        elif app.arguments.mode == AppMode.UPLOAD:
            scribe.bot.uploader.start(app)
        else:
            logging.error(f"Unknown argument for 'mode': {app.arguments.mode}")


# Main
#---------------------------------------------

if __name__ == "__main__":
    Program.main()
