"""See https://stackoverflow.com/questions/54106603 """

import click
import yaml
from .constants import CONFIG_STARTER_DICT, CONFIG_YAMLFILE_NAME
from .utils import update_settings_dict_from_config_yamlfile


class LoadInitForCommands(click.Group):
    def command(self, *args, **kwargs):
        def decorator(f):
            cmd = click.command(*args, **kwargs)(f)
            self.add_command(cmd)
            orig_invoke = cmd.invoke

            def invoke(ctx):
                ctx.obj = CONFIG_STARTER_DICT
                if cmd.name != "init":
                    config = yaml.load(open(CONFIG_YAMLFILE_NAME).read())
                    update_settings_dict_from_config_yamlfile(ctx.obj, config)

                return orig_invoke(ctx)

            cmd.invoke = invoke
            return cmd

        return decorator
