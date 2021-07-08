# -*- coding: utf-8 -*-
from datetime import datetime

from .request_api import RequestAPI


class RadarrAPIv3(RequestAPI):

    def construct_movie_json(
        self, dbId, qualityProfileId, rootDir, monitored=True, searchForMovie=True
    ):
        """Searches for movie on tmdb and returns Movie json to add

        Args:
            Required - dbID, <imdb or tmdb id>
            Required - qualityProfileId (int)
            Required - rootDir (string)
            Optional - monitored (boolean)
            Optional - searchForMovie (boolean)

        Return:
            JsonArray

        """
        s_dict = self.lookup_movie(dbId)
        print(s_dict)

        if not s_dict:
            raise Exception("Movie Doesn't Exist")

        movie_json = {
            "title": s_dict[0]["title"],
            "rootFolderPath": rootDir,
            "qualityProfileId": qualityProfileId,
            "year": s_dict[0]["year"],
            "tmdbId": s_dict[0]["tmdbId"],
            "images": s_dict[0]["images"],
            "titleSlug": s_dict[0]["titleSlug"],
            "monitored": monitored,
            "addOptions": {"searchForMovie": searchForMovie},
        }
        return movie_json

    ## MOVIE

    # GET /movie/ and /movie/{id}
    def get_movie(self, tmdbid=None):
        """get_movie returns all movies in collection.

        Args:
            Optional - tmdbid - TMDb id of the movie to get
        Returns:
            json response

        """
        if tmdbid:
            path = f"/api/v3/movie?tmdbId={int(tmdbid)}"
            print(path)
        else:
            path = "/api/v3/movie"
        res = self.request_get(path)
        return res

    # POST /movie
    def add_movie(
        self, dbId, qualityProfileId, rootDir=None, monitored=True, searchForMovie=True
    ):
        """addMovie adds a new movie to collection

        Args:
            Required - dbid tmdb id
            Required - qualityProfileId (int)
            Required - rootDir (string)
        Returns:
            json response

        """
        if not rootDir:
            rootDir = self.get_root()[0]["path"]

        term = f"tmdb:{str(dbId)}"

        movie_json = self.construct_movie_json(
            term, qualityProfileId, rootDir, monitored, searchForMovie
        )

        path = "/api/v3/movie"
        res = self.request_post(path, data=movie_json)
        return res

    # PUT /movie
    def update_movie(self, data):
        """Update an existing movie.

        Args:
            data (dictionary containing an object obtained by get_movie())
        Returns:
            json response
        """

        path = "/api/movie"
        res = self.request_put(path, data)
        return res

    # DELETE /movie/{id}
    def del_movie(self, movieId, delFiles=False, addExclusion=False):
        """Delete a single movie by database id
        Args:
            Required - movieId (int)
            Optional - delFiles (bool)
            Optional - addExclusion (bool)
        Returns:
            json response

        """
        # File deletion does not work
        data = {"deleteFiles": delFiles, "addExclusion": addExclusion}
        path = f"/api/v3/movie/{movieId}"
        res = self.request_del(path, data)
        return res

    # GET /movie/lookup
    def lookup_movie(self, term):
        """Searches for movie

        Args:
            Requried - term (uses tmdb for search results)
        Returns:
            json response

        """
        term = str(term)
        term = term.replace(" ", "%20")
        path = f"/api/v3/movie/lookup?term={term}"
        res = self.request_get(path)
        return res

    # TODO: PUT /movie/editor
    # TODO: DELETE /movie/editor
    # TODO: POST /movie/import

    ## MOVIEFILE

    # TODO: GET /moviefile

    # GET /moviefile/{id}
    def get_movie_file(self, movieId):
        """Returns movie files"""

        path = f"/api/v3/moviefile/{movieId}"
        res = self.request_get(path)
        return res

    # DELETE /moviefile/{id}
    def del_movie_file(self, movieId):
        """Allows for deletion of a moviefile by its database id.
        Args:
            Required - movieId (int)
        Returns:
            json response

        """
        path = f"/api/v3/movie/{movieId}"
        res = self.request_del(path)
        return res

    ## HISTORY

    # GET /history
    def get_history(
        self, page=1, pageSize=20, sortKey="date", sortDirection="descending"
    ):
        """Return a json object list of items in your history

        Args:
            Required - page (int) - Default: 1
            Required - pageSize (int) - Default: 20
            Required - sortKey (string) - Default: date
            Required - sortDir (string) - Default: descending
        Returns:
            json response
        """
        path = f"/api/v3/history?page={page}&pageSize={pageSize}&sortDirection={sortDirection}&sortKey={sortKey}"
        res = self.request_get(path)
        return res

    # GET /history/movie
    def get_history_movie(self, movieId, eventType=None):
        """Return a json object list of items in your history

        Args:
            Required - movieId (int) (Database id of movie)
            Optional - eventType (int) (History event type to retrieve)
        Returns:
            json response
        """
        if not eventType:
            path = f"/api/v3/history/movie?movieId={movieId}"
        else:
            path = f"/api/v3/history/movie?movieId={movieId}&eventType={eventType}"
        res = self.request_get(path)
        return res

    ## BLACKLIST

    # TODO: GET /blacklist
    # TODO: DELETE /blacklist
    # TODO: GET /blacklist/movie
    # TODO: DELETE /blacklist/bulk

    ## QUEUE

    # GET /queue
    def get_queue(
        self,
        page=1,
        pageSize=20,
        sortKey="timeLeft",
        sortDirection="ascending",
        includeUnknownMovieItems="true",
    ):
        """Return a json object list of items in the queue"""
        path = f"/api/v3/queue?page={page}&pageSize={pageSize}&sortDirection={sortDirection}&sortKey={sortKey}&includeUnknownMovieItems={includeUnknownMovieItems}"

        res = self.request_get(path)
        return res

    # TODO: DELETE /queue/{id}
    # TODO: DELETE /queue/bulk
    # TODO: GET /queue/details
    # TODO: GET /queue/status
    # TODO: POST /queue/grab/{id}

    ## INDEXER

    # GET /indexer and /indexer/{id}
    def get_indexer(self, id=None):
        """Get all indexers or a single indexer by its database id

        Args:
            Optional - id (int)
        Returns:
            json response
        """
        if not id:
            path = "/api/v3/indexer"
        else:
            path = f"/api/v3/indexer/{id}"

        res = self.request_get(path)
        return res

    # PUT /indexer/{id}
    # TODO: look into this, documentation lacking
    def put_indexer(self, id):
        """Edit an indexer"""
        path = f"/api/v3/indexer/{id}"
        res = path.request_put(path)
        return res

    # DELETE /indexer/{id}
    def del_indexer(self, id):
        """Delete and indexer

        Args:
            Required - id (int)
        Returns:
            json response
        """
        path = f"/api/v3/indexer/{id}"
        res = self.request_del(path)
        return res

    ## DOWNLOAD CLIENT

    # GET /downloadclient and /downloadclient/{id}
    def get_downloadclient(self, id=None):
        """Get all download clients or a single download client by its database id

        Args:
            Optional - id (int)
        Returns:
            json response
        """
        if not id:
            path = "/api/v3/downloadclient"
        else:
            path = f"/api/v3/downloadclient/{id}"

        res = self.request_get(path)
        return res

    # PUT /downloadclient/{id}
    # TODO: look into this, documentation lacking
    def put_downloadclient(self, id):
        """Edit an downloadclient"""
        path = f"/api/v3/downloadclient/{id}"
        res = path.request_put(path)
        return res

    # DELETE /downloadclient/{id}
    def del_downloadclient(self, id):
        """Delete an downloadclient

        Args:
            Required - id (int)
        Returns:
            json response
        """
        path = f"/api/v3/downloadclient/{id}"
        res = self.request_del(path)
        return res

    ## IMPORT LISTS

    # GET /importlist and /importlist/{id}
    def get_importlist(self, id=None):
        """Get all import lists or a single import list by its database id

        Args:
            Optional - id (int)
        Returns:
            json response
        """
        if not id:
            path = "/api/v3/importlist"
        else:
            path = f"/api/v3/importlist/{id}"

        res = self.request_get(path)
        return res

    # PUT /importlist/{id}
    # TODO: look into this, documentation lacking
    def put_importlist(self, id):
        """Edit an importlist"""
        path = f"/api/v3/importlist/{id}"
        res = path.request_put(path)
        return res

    # DELETE /importlist/{id}
    def del_importlist(self, id):
        """Delete an importlist

        Args:
            Required - id (int)
        Returns:
            json response
        """
        path = f"/api/v3/importlist/{id}"
        res = self.request_del(path)
        return res

    ## NOTIFICATION

    # GET /notification and /notification/{id}
    def get_notification(self, id=None):
        """Get all notifications or a single notification by its database id

        Args:
            Optional - id (int)
        Returns:
            json response
        """
        if not id:
            path = "/api/v3/notification"
        else:
            path = f"/api/v3/notification/{id}"

        res = self.request_get(path)
        return res

    # PUT /notification
    # TODO: look into this, documentation lacking
    def put_notification(self, id):
        """Edit a notification"""
        path = f"/api/v3/notification/{id}"
        res = path.request_put(path)
        return res

    # DELETE /notification
    def del_notification(self, id):
        """Delete a notification

        Args:
            Required - id (int)
        Returns:
            json response
        """
        path = f"/api/v3/notification/{id}"
        res = self.request_del(path)
        return res

    ## TAG

    # TODO: GET /tag
    # TODO: POST /tag
    # TODO: GET /tag/detail
    # TODO: GET /tag/detail/{id}
    # TODO: GET /tag/{id}
    # TODO: DELETE /tag/{id}
    # TODO: PUT /tag/{id}

    ## DISKSPACE

    # GET /diskspace
    def get_disk_space(self):
        """Query Radarr for disk usage information

            Location: System > Status

        Args:
            None
        Returns:
            json response

        """
        path = "/api/v3/diskspace"
        res = self.request_get(path)
        return res

    ## SETTINGS

    # GET /config/ui
    def get_config_ui(self):
        """Query Radarr for UI settings"""
        path = "/api/v3/config/ui"
        res = self.request_get(path)
        return res

    # PUT /config/ui
    def put_config_ui(self, data):
        """Edit one or many UI Settings and save to the database"""
        path = "/api/v3/config/ui"
        res = self.request_put(path, data)
        return res

    # GET /config/host
    def get_config_host(self):
        """Get General/Host settings for Radarr."""
        path = "/api/v3/config/host"
        res = self.request_get(path)
        return res

    # PUT /config/host
    def put_config_host(self, data):
        """Edit General/Host settings for Radarr."""
        path = "/api/v3/config/host"
        res = self.request_put(path, data)
        return res

    # GET /config/naming
    def get_config_naming(self):
        """Get Settings for movie file and folder naming."""
        path = "/api/v3/config/naming"
        res = self.request_get(path)
        return res

    # PUT /config/naming
    def put_config_naming(self, data):
        """Edit Settings for movie file and folder naming."""
        path = "/api/v3/config/naming"
        res = self.request_put(path, data)
        return res

    ## METADATA

    # GET /metadata
    def get_metadata(self):
        """Get all metadata consumer settings"""
        path = "/api/v3/metadata"
        res = self.request_get(path)
        return res

    ## SYSTEM

    # GET /system/status
    def get_system_status(self):
        """Find out information such as OS, version, paths used, etc"""
        path = "/api/v3/system/status"
        res = self.request_get(path)
        return res

    ## HEALTH

    # GET /health
    def get_health(self):
        """Query radarr for health information"""
        path = "/api/v3/health"
        res = self.request_get(path)
        return res

    ## COMMAND

    # POST /command
    def post_command(self, **kwargs):
        """Performs any of the predetermined Radarr command routines.

        Kwargs:
            Required - name (string).

            Options available:
                - ApplicationUpdate - Trigger an update of Radarr
                - Backup - Trigger a backup routine
                - CheckHealth - Trigger a system health check
                - ClearBlacklist - Triggers the removal of all blacklisted movies
                - CleanUpRecycleBin - Trigger a recycle bin cleanup check
                - DeleteLogFiles - Triggers the removal of all Info/Debug/Trace log files
                - DeleteUpdateLogFiles - Triggers the removal of all Update log files
                - DownloadedMoviesScan - Triggers the scan of downloaded movies
                - MissingMoviesSearch - Triggers a search of all missing movies
                - RefreshMonitoredDownloads - Triggers the scan of monitored downloads
                - RefreshMovie - Trigger a refresh / scan of library
                    - movieIds:int[] - a list of ids (comma separated) for movies to refresh

            See https://radarr.video/docs/api/#/Command/post-command
        Returns:
        json response

        """
        path = "/api/v3/command"

        data = kwargs
        res = self.request_post(path, data)
        return res

    ## UPDATE

    # GET /update
    def get_update(self):
        """Returns a list of recent updates to Radarr

        Location: System > Updates
        """
        path = "/api/v3/update"
        res = self.request_get(path)
        return res

    ## QUALITY PROFILE

    # GET /qualityProfile
    def get_quality_profiles(self):
        """Query Radarr for quality profiles"""
        path = "/api/v3/qualityProfile"
        res = self.request_get(path)
        return res

    ## CALENDAR

    # GET /calendar
    def get_calendar(self, unmonitored="true", start_date=None, end_date=None):
        """Get a list of movies based on calendar parameters.
        If start and end are not provided, retrieves movies airing today and tomorrow.

         args:
            Required - unmonitored (bool)
            Optional -
                - start_date (datetime ISO 8601):
                - end_date (datetime ISO 8601):

         Returns:
             json response

        """
        if start_date and end_date:
            if isinstance(start_date, datetime):
                startDate = start_date.strftime("%Y-%m-%d")

            if isinstance(end_date, datetime):
                endDate = end_date.strftime("%Y-%m-%d")
            path = f"/api/v3/calendar?unmonitored={unmonitored}&start_date={startDate}&end_date={endDate}"
        else:
            path = "/api/v3/calendar"
        res = self.request_get(path)
        return res

    ## CUSTOM FILTERS

    # GET /customfilter
    def get_custom_filter(self):
        """Query Radarr for custom filters."""
        path = "/api/v3/customfilter"
        res = self.request_get(path)
        return res

    ## REMOTE PATH MAPPING

    # GET /remotePathMapping
    def get_remote_path_mapping(self):
        """Get a list of remote paths being mapped and used by Radarr"""
        path = "/api/v3/remotePathMapping"
        res = self.request_get(path)
        return res

    ## ROOT FOLDER

    # GET /rootfolder
    def get_root(self):
        """Returns the Root Folder"""
        path = "/api/v3/rootfolder"
        res = self.request_get(path)
        return res
