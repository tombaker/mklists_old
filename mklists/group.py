"""See https://stackoverflow.com/questions/54106603 """

import click
import yaml


class LoadInitForCommands(click.Group):
    def command(self, *args, **kwargs):
        def decorator(f):
            cmd = click.command(*args, **kwargs)(f)
            self.add_command(cmd)
            orig_invoke = cmd.invoke

            def invoke(ctx):
                # Custom init code is here
                ctx.obj = {}
                if cmd.name != "init":
                    config = yaml.load(open(".configrc").read())
                    ctx.obj.update({key: config[key] for key in config})

                # call the original invoke()
                return orig_invoke(ctx)

            # hook the command's invoke
            cmd.invoke = invoke
            return cmd

        return decorator
