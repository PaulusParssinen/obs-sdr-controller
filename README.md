# OBS SDR Control

> [!CAUTION]
> The program is still in development. Do not use it in public broadcasts until it is stable.

> [!CAUTION]
> Under any circumstances, DO NOT share the `client_secret.json`, `token_secret.json` and `secrets.json` files in `config` directory to **anyone**.

## Contents

- [OBS SDR Control](#obs-sdr-control)
  - [Contents](#contents)
  - [Requirements](#requirements)
  - [Setup](#setup)
  - [Usage](#usage)
  - [Commands](#commands)
  - [Configuration](#configuration)
    - [SDRs](#sdrs)
      - [The fallback specification](#the-fallback-specification)
      - [The SDR specification](#the-sdr-specification)
      - [Rotation](#rotation)
      - [Presets](#presets)
        - [The preset specification](#the-preset-specification)
    - [OBS](#obs)
      - [`scenes`](#scenes)
      - [`browser_source`](#browser_source)
    - [Youtube](#youtube)
    - [Database](#database)

## Requirements

- Python 3.10 or higher (preferably the latest).
- OBS v27 or higher.
  - You must install [obs-websocket](https://github.com/obsproject/obs-websocket/releases) 5.x (tested on [5.0.1](https://github.com/obsproject/obs-websocket/releases/tag/5.0.1)) **if you're on OBS v27**. You do not need to install if you're on newer version.

## Setup

1. Download the repository to a directory you can find with:
   1. `git clone obs-sdr-controller`. Recommended for easier updating in future.
   2. or if your machine does not have `git`. Grab the repository as `zip` file and extract it to a directory of your choosing
2. In order to interact with the live broadcast chat, we need to use Youtube Data API. Follow the guide below or the official guide at https://developers.google.com/youtube/v3/live/getting-started#before-you-start
   1. Create a project in the [Google Developers Console](https://console.developers.google.com/).
   2. Search for YouTube Data API v3 and enable it. Now open YouTube Data API v3 management page.
   3. On the "Credentials" tab, click "Create credentials" and select "OAuth client ID".
   4. Select "Desktop app" as the application type and give it a name.
   5. Click "Create" and you will be presented with the client ID and client secret.
   6. Download and **rename** the file to `client_secret.json` and place it in the `config` directory. Never share the contents this file!
3. Launch command-line in the directory where the script was installed.
4. Install the required Python packages by running `pip install -r requirements.txt` in the terminal.
5. Configure the `config.json` file in the `config` directory to your liking. See the [Configuration](#configuration) section for more details.
6. Run the script by executing `python main.py` in the terminal.

## Usage

Launch the script by running `python main.py` in the terminal.

## Commands

> [!WARNING]
> This is still draft of the command to be implemented..

- `!preset [preset_id] [?freq]`
  - Switches to the specified preset and optionally overrides the frequency.
  - Examples:
    - `!preset 11175`
      - Switches to the preset with the id `11175`
    - `!preset channelone 31.7`
      - Switches to the preset with the id `channelone` and sets the frequency to `31.7`
- `!set [field] [value]`
  - Update any of the fields such `freq` _without_ updating the preset
- `!sdr [sdr_id] [?preset_id] [?freq]`
  - Switches to the configured SDR (and to the preset and frequency)
  - Examples:
    - `!sdr kph`
    - `!sdr lakesuperior channelone`
    - `!sdr gulf channelone 22.7`
- `!preset [id] set [field] [value]`
  - Edit the persistent preset values. Updates changes to the configuration file and if current preset; reloads the SDR.
  - Examples:
    - `!preset 11175 set zoom 10`
- `!fallback`
  - Resets to the `fallback` configuration.
- `!reload preset/config/browser`
  - Reloads the browser or the configuration file depending on the argument.
  - Examples:
    - `!reload preset`
      - Reloads the preset configuration. This will reload the browser with the current preset.
- **(ADMIN-ONLY)** `!users add/remove [user]`
  - TODO: need to test what format youtube uses for user livestream user ids
- **(ADMIN-ONLY)** `!mute on/off`
  - (Un)mutes the browser OBS source.
- **(ADMIN-ONLY)** `!stop`
  - Terminates the OBS broadcast.
- **(ADMIN-ONLY)** `!scene [obs_scene_name]`
  - Attempts to switch so the specified OBS scene if it exists.
  - Example:
    - `!scene StandByScene`

## Configuration

Almost everything about the scripts behavior can be configured in the `config.json` file in the `config` directory. The **secrets** such as the YouTube Data API credentials and are in the

### SDRs

#### The fallback specification

| Field  | Type | Required | Description                                |
| ------ | ---- | -------- | ------------------------------------------ |
| sdr    | Text | ✅       | The `id` of the SDR to use as fallback.    |
| preset | Text | ✅       | The `id` of the preset to use as fallback. |

#### The SDR specification

| Field    | Type | Required | Description                                                          |
| -------- | ---- | -------- | -------------------------------------------------------------------- |
| id       | Text | ✅       | A **unique** name used to identify this SDR.                         |
| url      | Text | ✅       | A well formed URL address of the SDR                                 |
| nickname | Text | No       | A human readable nickname (for display purposes)                     |
| preset   | Text | No       | The `id` of the preset to use upon load. Commands can override this. |

#### Rotation

TODO: Design the rotation automation logic and configuration.

#### Presets

_Presets_ are used to describe the actual SDR settings; the frequency, mode, zoom level and many other values.
These presets can be updated at any time by editing the configuration file and issuing a reload command, or by issuing preset update command.

The `base_preset` object is used to avoid repeating common values and to make changing them easier. All custom configurations in the `presets` array inherit the values from `base_preset` but any value can simply override any of them by specifying them in the actual preset.

**All custom presets must have an unique** `id` that is used to identify (e.g. when choosing a preset via command).

##### The preset specification

| Field                 | Type         | Default                              | Required | Description                                                                                                                                                                            |
| --------------------- | ------------ | ------------------------------------ | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`                  | Text         | -                                    | ✅       | A **unique** name used to identify this preset. Not used for `base_preset`.                                                                                                            |
| `obs_scene`           | Text         | -                                    | ✅       | The name of the OBS scene to use for this preset. Must match unique scene name specified in the [OBS section.](#obs)                                                                   |
| `inherit_base_preset` | `true/false` | `true`                               | No       | If set to `false`; this preset does not inherit any values from the `basePreset`                                                                                                       |
| `freq`                | Number       | -                                    | No       | The SDR frequency (in KHz)                                                                                                                                                             |
| `mode`                | Text         | -                                    | No       | The mode                                                                                                                                                                               |
| `zoom`                | Number       | -                                    | No       | Set the Waterfall zoom level, `0` (max-out) to `14` (max-in)                                                                                                                           |
| `volume`              | Number       | -                                    | No       | Volume from `0` to `200`                                                                                                                                                               |
| `pb_width`            | Text         | -                                    | No       | Set passband `width` (carrier centered) or `low,high`                                                                                                                                  |
| `pb_center`           | Text         | -                                    | No       | Set passband `center` using current width or `center,width`                                                                                                                            |
| `wf_colormap`         | Number       | `0`                                  | No       | Waterfall colormap: `0`=default, `1..n`=(others)                                                                                                                                       |
| `wf_speed`            | Text         | -                                    | No       | Waterfall speed: `0, off, 1, 1hz, s, slow, m, med, f, fast`                                                                                                                            |
| `wf_range`            | Text         | -                                    | No       | Waterfall `min{,max}`, e.g. `-110` or `-90,-70`                                                                                                                                        |
| `wf_auto`             | `true/false` | -                                    | No       | Waterfall auto (`=true`) or manual (`=false`) aperture mode                                                                                                                            |
| `wf_interpolation`    | Number       | `13` (Drop sampling with CIC filter) | No       | Waterfall interpolation: `0=Max`, `1=Min`, `2=Last`, `3=Drop` to `4=CMA` or respectively 10 to 14 with CIC filter.                                                                     |
| `wf_contrast`         | Number       | `0`                                  | No       | Waterfall contrast: `0=default, 1, 2, 3, 4`                                                                                                                                            |
| `mute`                | `true/false` | `false`                              | No       | Mute audio.                                                                                                                                                                            |
| `mem`                 | Text         | -                                    | No       | A preset frequency memory menu from comma-separated values. e.g. `4724,8992,11175`                                                                                                     |
| `keys`                | Text         | -                                    | No       | Sequence of keyboard shortcut keys to apply when connected                                                                                                                             |
| `user`                | Text         | -                                    | No       | Set "name/callsign" field                                                                                                                                                              |
| `password`            | Text         | -                                    | No       | Specify time limit / masked frequency exemption password                                                                                                                               |
| `extension`           | Text         | -                                    | No       | A extension configuration string, e.g. `fsk,ITA2,5N1V,shift:50,baud:50,inverted:1`. See [offical documentation for more details](http://www.kiwisdr.com/quickstart/#id-user-urlp-ext). |

### OBS

The OBS configurations consists of details needed to establish the WebSocket connection and the scene & source specific options.

> [!NOTE]
> The script relies on the OBS scene and source _names_ to identify whether it is owned by the script. This means they must be unique not changed without updating the configuration, otherwise script simply loses track of them. If the script can't find existing source or scene, it will create a new scene/source with correct name.

| Field                    | Type                      | Default | Required | Description                                                                                 |
| ------------------------ | ------------------------- | ------- | -------- | ------------------------------------------------------------------------------------------- |
| `websocket_port`         | Text                      | `4455`  | ✅       | The OBS WebSocket port.                                                                     |
| `placeholder_scene_name` | Text                      | -       | ✅       | Name of the scene to switch to when even the [fallback](#the-fallback-specification) fails. |
| `scenes`                 | [`scenes`](#scenes) array | -       | ✅       | List of OBS scenes to be used in presets                                                    |

#### `scenes`

| Field            | Type                                | Default | Required | Description                                                         |
| ---------------- | ----------------------------------- | ------- | -------- | ------------------------------------------------------------------- |
| `name`           | Text                                | -       | ✅       | **Unique** scene name used to keep track of the SDR browser source. |
| `browser_source` | [`browser_source`](#browser_source) | -       | ✅       | The browser source specification to be used in this scene.          |

#### `browser_source`

| Field                   | Type    | Default                                                                            | Required | Description                                                          |
| ----------------------- | ------- | ---------------------------------------------------------------------------------- | -------- | -------------------------------------------------------------------- |
| `name`                  | Text    | -                                                                                  | ✅       | **Unique** source name used to keep track of the SDR browser source. |
| `url`                   | Text    | `https://obsproject.com/browser-source`                                            | No       | The URL                                                              |
| `css`                   | Text    | `body { background-color: rgba(0, 0, 0, 0); margin: 0px auto; overflow: hidden; }` | No       | Custom CSS                                                           |
| `fps`                   | Text    | `30`                                                                               | No       | Custom frame rate. If set, `custom_fps` must be set `true`.          |
| `fps_custom`            | Boolean | `False`                                                                            | No       | See above.                                                           |
| `width`                 | Integer | `800`                                                                              | No       | The width of the browser.                                            |
| `Height`                | Integer | `600`                                                                              | No       | The height of the browser.                                           |
| `reroute_audio`         | Boolean | `False`                                                                            | No       | Control audio via OBS                                                |
| `restart_when_active`   | Boolean | `False`                                                                            | No       | -                                                                    |
| `shutdown`              | Boolean | `False`                                                                            | No       | -                                                                    |
| `webpage_control_level` | Integer | `1`                                                                                | No       | From 0 to                                                            |

### Youtube

YouTube configuration section is used to configure the YouTube Data API.

> [!NOTE]
>
> The `live_chat_poll_interval` is used to determine how often the script fetches new live broadcast comments to process. The default value is `10` seconds.
>
> The value is set to be the value you should be able use for 24/7 broadcast and avoid hitting the quota limits. For more information, see the official documentation at: [Quota and compliance audits](https://developers.google.com/youtube/v3/guides/quota_and_compliance_audits).

| Field                     | Type       | Default | Required | Description                                                                      |
| ------------------------- | ---------- | ------- | -------- | -------------------------------------------------------------------------------- |
| `live_chat_poll_interval` | Integer    | `10`    | ✅       | How often the script fetches new live broadcast comments to process (in seconds) |
| `admin_channel_ids`       | Text array | (Empty) |          | A list of YouTube channel IDs that are considered as admins.                     |
| `approved_channel_ids`    | Text array | (Empty) |          | A list of YouTube channel IDs that are considered as approved users.             |

### Database

The script uses local SQLite database to track some additional data, such as seen users, last SDR status and so on. The database is created automatically when the script is run for the first time.

The database is by default stored in the `data` directory as `database.db` file.

| Field             | Type | Default                      | Required | Description                            |
| ----------------- | ---- | ---------------------------- | -------- | -------------------------------------- |
| connection_string | Text | `sqlite:///data/database.db` | ✅       | The connection string to the database. |
