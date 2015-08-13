# docker-lloyd
*[Lloyd's Coffee House](http://en.wikipedia.org/wiki/Lloyd%27s_Coffee_House)
was the first marine insurance company.*

This tools backups Docker [volume containers](http://docs.docker.io/en/latest/use/working_with_volumes/#creating-and-mounting-a-data-volume-container)
and stores them on s3.

To use it, run:

    $ docker run -v /var/run/docker.sock:/docker.sock \
             -v /var/lib/docker/vfs/dir:/var/lib/docker/vfs/dir \
             -e ACCESS_KEY=... -e SECRET_KEY=... dckr/docker-lloyd \
              s3://<BUCKET> container-a container-b container-c...

This will run [docker-backup](https://github.com/docker-infra/docker-backup),
gzip and upload a tarball named after the container to S3.

Container uses environment variable, which can be overwritten:

| Variable | Default value | Description |
| -------- | ------------- | ----------- |
| PREFIX | "%Y-%m-%d_%H-%m-%S_" | Tarball prefix |
| SUFFIX | | Tarball suffix |
| TIMEOUT | 86400 | Backup period - 86400 = 24hours |

See [docker-backup](https://github.com/discordianfish/docker-backup) on
how to restore a backup.

The Dockerfile passes command line options to docker-backup by setting the OPTS
environment variable. If you need to override/change those, you can set it on
the command line:

    $ docker run -e OPTS="-addr=/foo/docker.sock" ...
