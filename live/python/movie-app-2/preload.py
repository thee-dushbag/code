from pathlib import Path
import typing as ty, config as cfg
from aiohttp import web
import click

app = ty.cast(web.Application, {})


@click.command
@click.help_option('--help', '-h')
@click.option(
    "--data-directory", type=click.Path(exists=True, file_okay=False, path_type=Path)
)
@click.option("--no-confirm-delete-thumbnail", is_flag=True, default=True)
@click.option("--no-confirm-delete-preview", is_flag=True, default=True)
@click.option("--no-confirm-junk-cleanup", is_flag=True, default=True)
@click.option("--reload-default-thumbnail", flag_value=True)
@click.option("--reload-default-preview", flag_value=True)
@click.option("--generate-thumbnails", flag_value=True)
@click.option("--cleanup-junk-files", flag_value=True)
@click.option("--retry-nonexisting", flag_value=True)
@click.option("--generate-previews", flag_value=True)
@click.option("--process-statics", flag_value=True)
@click.option("--default-height", type=int, default=256)
@click.option("--default-width", type=int, default=512)
@click.option("--dry-run", flag_value=True)
@click.option("--run", "-r", flag_value=True)
def main(
    default_width: int,
    default_height: int,
    data_directory: Path,
    generate_previews: bool,
    generate_thumbnails: bool,
    cleanup_junk_files: bool,
    no_confirm_delete_preview: bool,
    no_confirm_delete_thumbnail: bool,
    no_confirm_junk_cleanup: bool,
    process_statics: bool,
    retry_nonexisting: bool,
    reload_default_thumbnail: bool,
    reload_default_preview: bool,
    dry_run: bool,
    run: bool,
):
    "Use <command> --run/--dry-run to run the app. Just a workaround. (*_*) or atleast with one option, any option."
    if data_directory:
        data_directory = data_directory.absolute()
    sizes = abs(default_width), abs(default_height)
    if dry_run:
        from rich import get_console

        console = get_console()
        if data_directory is not None:
            if not cfg.RESOURCE_DIR.is_symlink():
                console.log(
                    f"The current data_directory is not a symlink: {cfg.RESOURCE_DIR!r}",
                )
            console.log(
                f"Create a symbolink link from {cfg.RESOURCE_DIR!s} to {data_directory!s}"
            )
        if reload_default_preview:
            console.log(f"Deleting default preview: {cfg.DEFAULT_PREVIEW!s}")
        if reload_default_thumbnail:
            console.log(f"Deleting default thumbnail: {cfg.DEFAULT_THUMBNAIL!s}")
        console.log("Setting options to")
        console.print(
            dict(
                data_directory=data_directory,
                generate_previews=generate_previews,
                generate_thumbnails=generate_thumbnails,
                cleanup_junk_files=cleanup_junk_files,
                confirm_delete_preview=no_confirm_delete_preview,
                confirm_delete_thumbnail=no_confirm_delete_thumbnail,
                confirm_junk_cleanup=no_confirm_junk_cleanup,
                process_statics=process_statics,
                retry_nonexisting=retry_nonexisting,
                reload_default_thumbnail=reload_default_thumbnail,
                reload_default_preview=reload_default_preview,
                default_height=sizes[1],
                default_width=sizes[0],
            )
        )
    else:
        if data_directory is not None:
            if not cfg.RESOURCE_DIR.is_symlink():
                click.echo(
                    f"The current data_directory is not a symlink: {cfg.RESOURCE_DIR!r}",
                    err=True,
                )
                exit(2)
            cfg.RESOURCE_DIR.unlink()
            cfg.RESOURCE_DIR.symlink_to(data_directory)
        if reload_default_preview:
            cfg.DEFAULT_PREVIEW.unlink()
        if reload_default_thumbnail:
            cfg.DEFAULT_THUMBNAIL.unlink()

        config = cfg.Config(
            generate_previews=generate_previews,
            generate_thumbnails=generate_thumbnails,
            cleanup_junk_files=cleanup_junk_files,
            confirm_delete_preview=no_confirm_delete_preview,
            confirm_delete_thumbnail=no_confirm_delete_thumbnail,
            confirm_junk_cleanup=no_confirm_junk_cleanup,
            process_statics=process_statics,
            retry_nonexisting=retry_nonexisting,
            defaults_size=sizes,
        )
        cfg.setup(app, config)


if __name__ == "__main__":
    main()
    # ...
