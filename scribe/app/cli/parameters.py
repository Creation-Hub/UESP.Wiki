from argparse import ArgumentParser

class Parameters:
    @staticmethod
    def create() -> ArgumentParser:
        """
        Defines the command line parameter parser.
        """

        parser:ArgumentParser = ArgumentParser(
            prog="scribe",
            description="Provides a command line interface for wiki automation tasks.",
        )

        # App
        parser.add_argument(
            "--settings",
            type=str,
            help="Path to the application settings JSON file."
        )


        # Logging
        parser.add_argument(
            "--log-date-format",
            type=str,
            help="Date format for log messages.",
        )

        parser.add_argument(
            "--log-console-level",
            type=str,
            help="The log level to use (DEBUG, INFO, WARNING, ERROR, CRITICAL)."
        )

        parser.add_argument(
            "--log-file-level",
            type=str,
            help="The log level to use (DEBUG, INFO, WARNING, ERROR, CRITICAL)."
        )

        parser.add_argument(
            "--log-file-path",
            type=str,
            help="The log file path to use."
        )


        # MODES
        modes = parser.add_subparsers(
            dest="mode",
            help="Start this application in 'generate' mode or 'upload' mode.",
            required=True
        )


        # Generator
        generate:ArgumentParser = modes.add_parser(
            "generate",
            help="Parse Papyrus scripts and generate MediaWiki files."
        )
        generate.add_argument(
            "--config",
            type=str
        )


        # Uploader
        upload:ArgumentParser = modes.add_parser(
            "upload",
            help="Upload generated MediaWiki files to the wiki via API."
        )

        upload.add_argument(
            "--config",
            type=str
        )

        upload.add_argument(
            "--environment",
            type=str
        )

        return parser
