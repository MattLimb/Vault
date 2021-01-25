# Vault

Vault is an offline, personal, password protected and encrypted file Vault. This spec is for all the features that need to be included within the Vault CLI tool version 1.0.

All 0.* versions are going to be alpha builds. A 1.0 beta will be released after all features in this document have been added. Once everything has been tested, and confirmed to be working as intended, an official 1.0 will be released on GitHub.

---

- [Vault](#vault)
  - [Vault Data](#vault-data)
    - [User Information](#user-information)
    - [Vault Information](#vault-information)
  - [Logging](#logging)
  - [Vault Ouputs](#vault-ouputs)
    - [0.1 - Text](#01---text)
    - [0.1 - JSON](#01---json)
    - [0.1 - XML](#01---xml)
    - [0.3 - CSV](#03---csv)
    - [Options](#options)
  - [Vault Management](#vault-management)
    - [0.1 - `vault new <filepath>`](#01---vault-new-filepath)
      - [Options](#options-1)
      - [Arguments](#arguments)
      - [Output](#output)
    - [0.1 - `vault delete <vault_name>`](#01---vault-delete-vault_name)
      - [Options](#options-2)
      - [Arguments](#arguments-1)
      - [Output](#output-1)
    - [0.1 - `vault rename <vault_name> <new_vault_name>`](#01---vault-rename-vault_name-new_vault_name)
      - [Options](#options-3)
      - [Arguments](#arguments-2)
      - [Output](#output-2)
    - [0.1 - `vault list`](#01---vault-list)
      - [Options](#options-4)
      - [Output](#output-3)
    - [0.1 - `vault show <vault_name>`](#01---vault-show-vault_name)
      - [Options](#options-5)
      - [Argument](#argument)
      - [Output](#output-4)
    - [0.1 - `vault default <vault_name>`](#01---vault-default-vault_name)
      - [Options](#options-6)
      - [Arguments](#arguments-3)
      - [Outputs](#outputs)
    - [`vault export <vault_name> <file_path>` - WIP](#vault-export-vault_name-file_path---wip)
    - [`vault import <file_path> <vault_name>` - WIP](#vault-import-file_path-vault_name---wip)
    - [`vault backup <vault_name>` - WIP](#vault-backup-vault_name---wip)
  - [### `vault archive <vault_name>`  - WIP](#-vault-archive-vault_name----wip)
  - [Group Actions](#group-actions)
    - [0.2 - `group new <group_name>`](#02---group-new-group_name)
      - [Options](#options-7)
      - [Arguments](#arguments-4)
      - [Output](#output-5)
    - [0.2 - `group delete <group_name>`](#02---group-delete-group_name)
      - [Options](#options-8)
      - [Arguments](#arguments-5)
      - [Output](#output-6)
    - [0.2 - `group rename <group_name> <new_group_name>`](#02---group-rename-group_name-new_group_name)
      - [Options](#options-9)
      - [Arguments](#arguments-6)
      - [Output](#output-7)
    - [0.2 - `group show <group_name>`](#02---group-show-group_name)
      - [Options](#options-10)
      - [Argument](#argument-1)
      - [Output](#output-8)
    - [0.3 - `group file add <group_name> <file_name>` - WIP](#03---group-file-add-group_name-file_name---wip)
    - [0.3 - `group file delete <group_name> <file_name>` - WIP](#03---group-file-delete-group_name-file_name---wip)
    - [0.3 - `group file show <group_name> <file_name>` - WIP](#03---group-file-show-group_name-file_name---wip)
  - [File/Folder Actions](#filefolder-actions)
    - [0.3 - `file add <file_name>`](#03---file-add-file_name)
      - [Options](#options-11)
      - [Arguments](#arguments-7)
      - [Output](#output-9)
    - [0.3 - `file retrieve <output> <file_name>`](#03---file-retrieve-output-file_name)
      - [Options](#options-12)
      - [Arguments](#arguments-8)
      - [Output](#output-10)
    - [0.3 - `file delete <file_name>`](#03---file-delete-file_name)
      - [Options](#options-13)
      - [Arguments](#arguments-9)
      - [Output](#output-11)
    - [0.3 - `file rename <file_name> <new_file_name>`](#03---file-rename-file_name-new_file_name)
      - [Options](#options-14)
      - [Arguments](#arguments-10)
      - [Output](#output-12)
    - [0.3 - `file replace <file_name> <filepath`](#03---file-replace-file_name-filepath)
      - [Options](#options-15)
      - [Arguments](#arguments-11)
      - [Output](#output-13)
    - [0.3 - `file show <file_name>`](#03---file-show-file_name)
      - [Options](#options-16)
      - [Arguments](#arguments-12)
      - [Output](#output-14)
  - [Generate](#generate)
    - [0.1 - `generate password`](#01---generate-password)
      - [Output](#output-15)
    - [0.1 - `generate hash <hash_algorithm> <file_path>`](#01---generate-hash-hash_algorithm-file_path)
      - [Arguments](#arguments-13)
      - [Output](#output-16)
    - [0.1 - `generate encryption-key`](#01---generate-encryption-key)
      - [Output](#output-17)
    - [0.5 - `generate name`](#05---generate-name)
    - [0.1 - `generate uuid`](#01---generate-uuid)
      - [Output](#output-18)
  - [Arbitrary Encryption and Decryption](#arbitrary-encryption-and-decryption)
    - [0.4 - `encrypt <file_name>`](#04---encrypt-file_name)
    - [0.4 - `decrypt <file_name>`](#04---decrypt-file_name)
  - [Versioning and Update](#versioning-and-update)
    - [0.1 - `version`](#01---version)
      - [Options](#options-17)
      - [Ouput](#ouput)
    - [0.4 - `update`](#04---update)
  - [PyPi Packages Needed](#pypi-packages-needed)

---

## Vault Data

Vault needs to store some key information about each Vault to provide the best experience to the user. Vault has two different categories of information that it needs to store: User and Vault Specific.

### User Information

User information, is global information that relates to a specific user account. Vault operates on a per user basis, which means that a user can only see, and interact with their own Vaults.

User information is held in a folder called `.vault` in the user's home directory: 

- Windows: `C:\Users\<username>\.vault\` 
- *nix: `~/.vault/` (`/home/<username>/.vault/` usually)

### Vault Information

Vault information is information that pertains to a specific vault. This information includes information on files. File information is generally:

- Vault File UUID
- File name
- File extension
- File mime
- File group
- Date Added
- Date Modified (File Rename/Update)
- File encryption key (encrypted with master password)
- Hash of the unencrypted file (anti-tamper)
- Hash of the encrypted file (anti-tamper)
- Folder structure
- Folder UUID
- Encrypted Key

This information is to be stored in a SQLite3 Database stored in the `.vault/files/<uuid>.db` folder in the home directory, under the UUID of the vault.

---
## Logging

---
## Vault Ouputs

This applies to everything except the help commands.

All Vault Commands that produce an output, should have the ability to be shown in a variety of formats. The format choices are the following:

- 0.1 - Text
- 0.1 - JSON
- 0.1 - XML
- 0.3 - CSV

### 0.1 - Text

This will be standard output text, as seen in the output examples of the below commands.

### 0.1 - JSON

This will be in prettified JSON, which will be outputted to the standard output.

This is for simpe message types, including errors:

```json
{
  "error": 0,
  "message": "Filename \"test_file.txt\" added",
  "vault": "<vault_name>"
}
```

This is for more complex message types:

```json
{
  "error": 0,
  "message": "Showing Vaults matching <vault_name>",
  "vault": null,
  "data": [
    {
      "vault": "vault_name",
      ...
    }
  ]
}
```

### 0.1 - XML

This will be in prettified XML, which will be outputted to the standard output and based on the JSON spec

This is for simpe message types, including errors:

```xml
<vaut_output>
  <error number=0 />
  <message>Filename \"test_file.txt\" added</message>
  <vault name="<vault_name>">
</vault_output>
```

This is for more complex message types:

```xml
<vaut_output>
  <error number=0 />
  <message>Filename \"test_file.txt\" added</message>
  <vault name="<vault_name>">
  <data>
    <vault name="<vault_name">
      <uuid></uuid>
      ...
    </vault>
  </data>
</vault_output>
```

### 0.3 - CSV

### Options

| Option          | Type | Description                        |
| :-------------: | :--: | ---------------------------------- |
| `-o`/`--output` | flag | The format the output should be in |

---

## Vault Management

### 0.1 - `vault new <filepath>`

This command creates a new Vault in the directory specified in the `filepath` argument. This command will take in a name and a master password for the Vault. This will prompt for the Name and Password - as they are required options.

The initial folder for the Vault will be left blank, ready to be populated by encrypted files.

This command will also add the following to the `vaults` key of the `vault.yaml`:

```yaml
<vault_uuid>:
  name: <vault_name>
  filepath: <vault_filepath>
  nonce: <vault_nonce>
  sanity: <vault_sanity_check>
  default: false
  added: <vault_added_date>
  modified: <vault_last_modified>
```

If this is the only vault listed, `default` will equal `true`, otherwise it will equal `false`.

#### Options

| Option            | Type  | Description                |
| :---------------: | :---: | -------------------------- |
| `-n`/`--name`     | `str` | A friendly name of a Vault |
| `-p`/`--password` | `str` | The Vault master password  |
| `-d`/`--debug`  | flag  | Enable debug logging       |

#### Arguments

| Argument   | Type  | nargs | Description                   |
| :--------: | :---: | :---: | ----------------------------- |
| `filepath` | `str` | 1     | The filepath of the new vault |

#### Output

The output of this command is going to be this for a success and the last message will be in green:

```sh
> vault vault new --name="New Vault" ./new_vault
Please Enter A Password: 
Please Confirm Your Password:

Vault 'New Vault' Created
```

The output of this command is going to be this for a error and the last message will be in red:

```sh
> vault vault new --name="New Vault" ./new_vault
Please Enter A Password: 
Please Confirm Your Password:

Error: Could not create new vault
```

### 0.1 - `vault delete <vault_name>`

This command deletes a vault by name or by UUID, if empty. This command will prompt the user to confirm deletion. The command will also delete the relevant YAML section after the folders have been deleted. 

#### Options

| Option            | Type  | Description                        |
| :---------------: | :---: | ---------------------------------- |
| `-p`/`--password` | `str` | The Vault master password          |
| `-d`/`--debug`  | flag  | Enable debug logging               |
| `-f`/`--force`    | flag  | Force delete vault, with all files |
| `-y`/`--yes`      | flag  | Confirm the deletion of the vault  |
| `-n`/`--no`       | flag  | Always deny the prompt             |

#### Arguments

| Argument     | Type  | nargs | Description                         |
| :----------: | :---: | :---: | ----------------------------------- |
| `vault_name` | `str` | >1    | The names of the vault(s) to delete |

#### Output

The output of this command is going to be this for a success and the last message will be in green:

```sh
> vault vault delete "New Vault"
Please Enter Your Password:

You are about to delete "New Vault". Deleting Vaults is irreversable.
Would you like to continue [y/n]: y

Vault 'New Vault' Deleted
```

The output of this command is going to be this for a error and the last message will be in red:

```sh
> vault vault delete "New Vault"
Please Enter Your Password:

You are about to delete "New Vault". Deleting Vaults is irreversable.
Would you like to continue? [y/N]: y

Error: Vault 'New Vault' could not be deleted.
```

Error Messages:

- Error: Cannot find Vault with name "<vault_name>" for this user
- Error: Vault "<vault_name>" contains files. Decrypt all files from this Vault, or use "-f" to remove them all
- Error: A file in Vault "<vault_name>" is open in another process. Please close the process which has "<file_name>" open.
- Error: Unknown Error - <error_message>

### 0.1 - `vault rename <vault_name> <new_vault_name>`

Vault friendly names are intended for the users to be able to identify what a Vault is, and what it does. Sometimes a Vault changes purpose, and direction, so they need another name to help the user identify the usecase for the Vault. 

This command provides an method to change the name of any Vault for the user with a new name. This command will prompt the user if they really want to do this.

#### Options

| Option           | Type | Description            |
| :--------------: | :--: | ---------------------- |
| `-d`/`--debug` | flag | Enable debug logging   |
| `-y`/`--yes`     | flag | Confirm the rename     |
| `-n`/`--no`      | flag | Always deny the prompt |


#### Arguments

| Argument         | Type  | nargs | Description                         |
| :--------------: | :---: | :---: | ----------------------------------- |
| `vault_name`     | `str` | 1     | The names of the vault(s) to delete |
| `new_vault_name` | `str` | 1     | The new name of the vault           |

#### Output

The output of this command is going to be this for a success and the last message will be in green:

```sh
> vault vault rename "New Vault" "Pictures Vault"
Please Enter Your Password:

You are about to rename "New Vault" to "Pictures Vault". Renaming Vaults is irreversable.
Would you like to continue? [y/N]: y

Vault "New Vault" renamed to "Pictures Vault"
```

The output of this command is going to be this for an error and the last message will be in red:

```sh
> vault vault rename "New Vault" "Pictures Vault"
Please Enter Your Password:

You are about to rename "New Vault" to "Pictures Vault". Renaming Vaults is irreversable.
Would you like to continue? [y/N]: y

Error: Vault 'New Vault' could not be renamed.
```

Error Messages:

- Error: Cannot find Vault with name "<vault_name>" for this user
- Error: Unknown Error - <error_message>

### 0.1 - `vault list`

Knowing which Vaults are availiable to a user is important for a user who uses the Vaults infrequently. This command will generate a list of names for each Vault known to the user. 

`-i` will display all the information for each vault present, similarly to [`vault info <vault_name>`](#vault-info-vault_name). 

#### Options

| Option            | Type  | Description                           |
| :---------------: | :---: | ------------------------------------- |
| `-d`/`--debug`  | flag  | Enable debug logging                  |
| `-i`/`--info`     | flag  | Retrieve information about each vault |

#### Output

The output of this command is going to be this for a success and the last message will be in white:

```sh
> vault vault list
Please Enter Your Password:

Vault: New Vault
Vault: Pictures Vault
Vault: Videos Vault
```

The output of this command is going to be this for an error and the last message will be in red:

```sh
> vault vault list
Please Enter Your Password:

Error: Cannot find Vaults for this user - No Vaults created
```

Error Messages:

- Error: Cannot find Vaults for this user - No Vaults created

### 0.1 - `vault show <vault_name>`

This command gives most of the information known about a Vault. The information will contain the following:

- Vault Name
- Vault UUID
- Vault Filepath
- Vault Creation Date
- Vault Last Modified Date (Last Time a File was Added)
- Number of Files in the Vault
- On-Disk Size of the Vault

#### Options

| Option            | Type  | Description                           |
| :---------------: | :---: | ------------------------------------- |
| `-d`/`--debug`  | flag  | Enable debug logging                  |

#### Argument

| Argument     | Type  | nargs | Description                         |
| :----------: | :---: | :---: | ----------------------------------- |
| `vault_name` | `str` | >=0   | The names of the vault(s) to delete |

#### Output

The output of this command is going to be this for a success and the last message will be in white:

```sh
> vault vault show

Vault:           New Vault
UUID:            <vault_uuid>
Location:        <vault_location>
Created:         <vault_created>
Last Modified:   <vault_modified>
Files In Vault:  <vault_files>
Size of Vault:   <vault_size>

Vault:           Pictures Vault
UUID:            <vault_uuid>
Location:        <vault_location>
Created:         <vault_created>
Last Modified:   <vault_modified>
Files In Vault:  <vault_files>
Size of Vault:   <vault_size>
```

The output of this command is going to be this for an error and the last message will be in red:

```sh
> vault vault show

Error: Cannot find Vaults for this user - No Vaults created
```

Error Messages:

- Error: Cannot find Vaults for this user - No Vaults created

### 0.1 - `vault default <vault_name>`

This command sets the default Vault to the `<vault_name>`. If no arguments is specified it will return the name of the default Vault.

#### Options

| Option            | Type  | Description                           |
| :---------------: | :---: | ------------------------------------- |
| `-d`/`--debug`  | flag  | Enable debug logging                  |

#### Arguments

| Argument     | Type  | nargs  | Description                         |
| :----------: | :---: | :----: | ----------------------------------- |
| `vault_name` | `str` | 0 or 1 | The names of the vault(s) to delete |


#### Outputs

This will be the output of the success criteria and it will be in green:

```sh
> vault vault default "New Vault"

Default Vault is: "New Vault"
```

If no argument is specified then the following is returned in green:

```sh
> vault vault default

Default Vault is "New Vault"
```

The following is the error condition and will be shown in red: 

```sh
> vault vault default "New Vault"

Error: Vault "New Vault" does not exist
```

Error Messages

- Error: Vault "<vault_name>" does not exist
- Error: There are no Vaults for this user

### `vault export <vault_name> <file_path>` - WIP

### `vault import <file_path> <vault_name>` - WIP

### `vault backup <vault_name>` - WIP

### `vault archive <vault_name>`  - WIP
---

## Group Actions

### 0.2 - `group new <group_name>`

Group add will add a new group to the Vault. These are going to be stored in the SQLite DB of the Vault. 

This will consist of two tables: `groups` and `group_files`.

`groups`:

- UUID (Primary Key)
- Name
- Created
- Modified

`group_files`:

- UUID - (Auto Increment Row Number)
- Group UUID (Foreign Key)
- File UUID (Foreign Key)

#### Options

| Option             | Type  | Description                                          |
| :----------------: | :---: | ---------------------------------------------------- |
| `-p`/`--password`  | `str` | The Vault master password                            |
| `-d`/`--debug`     | flag  | Enable debug logging                                 |
| `-v`/`--vault`     | `str` | The vault name                                       |

#### Arguments

| Argument     | Type  | nargs | Description                                |
| :----------: | :---: | :---: | ------------------------------------------ |
| `group_name` | `str` | >1    | The names of the groups to add to Vault    |

#### Output

The output will be colour coded. Successes are in Green, and errors are in Red.

```sh
> vault group add new_group
Please Enter Your Password:

Group "new_group" Created
```

An error condition would look like:

```sh
> vault group add new_group
Please Enter Your Password:

Error: "new_group" already exists
```

Error Messages:

- Error: "new_group" already exists
- Error: "<vault_name>" does not exist

### 0.2 - `group delete <group_name>`

This command is designed to delete a group. This will also prompt the user with a confirmation prompt to prompt them if they want to do it or not. 

#### Options

| Option            | Type  | Description                                                |
| :---------------: | :---: | ---------------------------------------------------------- |
| `-p`/`--password` | `str` | The Vault master password                                  |
| `-d`/`--debug`    | flag  | Enable debug logging                                       |
| `-v`/`--vault`    | `str` | The vault name                                             |
| `-y`/`--yes`      | flag  | Confirm the prompt                                         |
| `-n`/`--no`       | flag  | Always deny the prompt                                     |
| `-f`/`--files`    | flag  | Delete the files associated with the group as well         |


#### Arguments

| Argument     | Type  | nargs | Description                                |
| :----------: | :---: | :---: | ------------------------------------------ |
| `group_name` | `str` | >1    | The names of the groups to delete          |

#### Output

The output will be colour coded - Successes will be in green, and errors will be in red. 

Successful output will look like this:

```sh
> vault group delete test_group
Please Enter Your Password:

You are about to delete "test_group". Deleting groups is irreversable.
Would you like to continue? [y/N]: y

Group "test_group" deleted
```

Error conditions will look like this:

```sh
> vault group delete test_group
Please Enter Your Password:

You are about to delete "test_group". Deleting groups is irreversable.
Would you like to continue? [y/N]: y

Error: Group "<group_name>" not found
```

Error Messages:

- Error: Group "<group_name>" not found

### 0.2 - `group rename <group_name> <new_group_name>`

This command is designed to rename a group. This will also prompt the user with a confirmation prompt to prompt them if they want to do it or not. 

#### Options

| Option            | Type  | Description                                                |
| :---------------: | :---: | ---------------------------------------------------------- |
| `-p`/`--password` | `str` | The Vault master password                                  |
| `-d`/`--debug`    | flag  | Enable debug logging                                       |
| `-v`/`--vault`    | `str` | The vault name                                             |
| `-y`/`--yes`      | flag  | Confirm the prompt                                         |
| `-n`/`--no`       | flag  | Always deny the prompt                                     |


#### Arguments

| Argument         | Type  | nargs | Description                                |
| :--------------: | :---: | :---: | ------------------------------------------ |
| `group_name`     | `str` | 1     | The names of the file(s) to add into Vault |
| `new_group_name` | `str` | 1     | The new name of the group                  |

#### Output

The output will be colour coded - Successes will be in green, and errors will be in red. 

Successful output will look like this:

```sh
> vault group rename test_group renamed_group
Please Enter Your Password:

You are about to rename "test_group" to "renamed_group". Renaming groups is irreversable.
Would you like to continue? [y/N]: y

Group "test_group" renamed to "renamed_group"
```

Error conditions will look like this:

```sh
> vault group rename test_group renamed_group
Please Enter Your Password:

You are about to rename "test_group" to "renamed_group". Renaming groups is irreversable.
Would you like to continue? [y/N]: y

Error: Group "test_group" not found
```

Error Messages:

- Error: Group "<group_name>" not found

### 0.2 - `group show <group_name>`

This command gives most of the information known about a Group. The information will contain the following:

- Group Name
- Group UUID
- Group Creation Date
- Group Last Modified Date (Last Time a File was Added)
- Number of Files in the Group
- On-Disk Size of the Group

#### Options

| Option         | Type | Description          |
| :------------: | :--: | -------------------- |
| `-d`/`--debug` | flag | Enable debug logging |

#### Argument

| Argument     | Type  | nargs | Description                       |
| :----------: | :---: | :---: | --------------------------------- |
| `vault_name` | `str` | >=0   | The names of the vault(s) to show |

#### Output

The output of this command is going to be this for a success and the last message will be in white:

```sh
> vault group show

Group:           Default Group
UUID:            <group_uuid>
Created:         <group_created>
Last Modified:   <group_modified>
Files In Vault:  <group_files>
Size of Vault:   <group_size>

Group:           Docx Group
UUID:            <group_uuid>
Created:         <group_created>
Last Modified:   <group_modified>
Files In Vault:  <group_files>
Size of Vault:   <group_size>
```

The output of this command is going to be this for an error and the last message will be in red:

```sh
> vault group show

Error: Cannot find Groups for this user - No Groups created
```

Error Messages:

- Error: Cannot find Vaults for this user - No Vaults created

### 0.3 - `group file add <group_name> <file_name>` - WIP

### 0.3 - `group file delete <group_name> <file_name>` - WIP

### 0.3 - `group file show <group_name> <file_name>` - WIP

## File/Folder Actions

### 0.3 - `file add <file_name>`

This will encrypt a file, and add it to the specified Vault. By default, this will add the file to the default Vault, and will error if no Vault has been created. 

This will gather all the information needed for storing the file in the files database for the Vault. 

#### Options

| Option             | Type  | Description                                          |
| :----------------: | :---: | ---------------------------------------------------- |
| `-p`/`--password`  | `str` | The Vault master password                            |
| `-d`/`--debug`     | flag  | Enable debug logging                                 |
| `-v`/`--vault`     | `str` | The vault name                                       |
| `-f`/`--file-name` | `str` | The filename to store in the database                |
| `-g`/`--group`     | `str` | The group to add the file too                        |
| `-R`/`--recursive` | `str` | Add all files found in this folder to the Vault      |
| `-r`/`--remove`    | `str` | Delete the original file once encrypted in the Vault |

#### Arguments

| Argument    | Type  | nargs | Description                                |
| :---------: | :---: | :---: | ------------------------------------------ |
| `file_name` | `str` | >1    | The names of the file(s) to add into Vault |

#### Output

The output of the commands will be colour coded, so users can immediately see if the operations have been successfull or not. 

A success message would be in green and look like this:

```sh
> vault file add ./new_file.txt
Please Enter Your Password:

Added "./new_file.txt" to Vault "<vault_name>"
```

And multiple sucesses would be:

```sh
> vault file add ./new_file.txt ./new_new_file.txt
Please Enter Your Password:

Added "./new_file.txt" to Vault "<vault_name>"
Added "./new_new_file.txt" to Vault "<vault_name>"
```

Error messages would be in red and look like this:

```sh
> vault file add ./new_file.txt
Please Enter Your Password:

Error: File "./new_file.txt" does not exist.
```

Error messages:

- Error: File "<file_name>" does not exist
- Error: IO Error - Cannot open or read "<file_name>"

### 0.3 - `file retrieve <output> <file_name>`

This command will decrypt a file or folder or group into an output directory. This will take in the Vault master password, and will use the default Vault if none is specified. This command will NOT delete the files from the Vault.

#### Options

| Option            | Type  | Description                                                |
| :---------------: | :---: | ---------------------------------------------------------- |
| `-p`/`--password` | `str` | The Vault master password                                  |
| `-d`/`--debug`    | flag  | Enable debug logging                                       |
| `-v`/`--vault`    | `str` | The vault name                                             |
| `-p`/`--preserve` | flag  | Preserve folder structure of groups of files, or folders   |
| `-g`/`--group`    | flag  | Force the `<file_name>` argument to be a group id or name  |
| `-f`/`--folder`   | flag  | Force the `<file_name>` argument to be a folder id or name |
| `-l`/`--file`     | flag  | Force the `<file_name>` argument to be a file id or name   |

#### Arguments

| Argument    | Type  | nargs | Description                                    |
| :---------: | :---: | :---: | ---------------------------------------------- |
| `file_name` | `str` | >1    | The names of the file(s) to add into Vault     |
| `output`    | `str` | 1     | The output directory to decrypt the files into |

#### Output

The output will be colour coded - Successes will be in green, and errors will be in red. 

Successful output will look like this:

```sh
> vault file retrieve ./output_dir test_file.txt
Please Enter Your Password:

Decryption Complete - File found at ./output_dir/test_file.txt
```

Error conditions will look like this:

```sh
> vault file retrieve ./output_dir test_file.txt
Please Enter Your Password:

Error: File "<file_name>" not found
```

Error Messages:

- Error: File "<file_name>" not found
- Error: Cannot find group "<file_name>". Please remove the -g/--group flags to automatically search for a match.
- Error: Cannot find folder "<file_name>". Please remove the -f/--folder flags to automatically search for a match.
- Error: Cannot find output folder "<folder_name>"
- Error: Cannot create output folder "<folder_name>"

### 0.3 - `file delete <file_name>`

This command is designed to delete a file, folder or group from the Vault. This will include all files specified in the group or folder. This will also prompt the user with a confirmation prompt to prompt them if they want to do it or not. 

#### Options

| Option            | Type  | Description                                                |
| :---------------: | :---: | ---------------------------------------------------------- |
| `-p`/`--password` | `str` | The Vault master password                                  |
| `-d`/`--debug`    | flag  | Enable debug logging                                       |
| `-v`/`--vault`    | `str` | The vault name                                             |
| `-f`/`--folder`   | flag  | Force the `<file_name>` argument to be a folder id or name |
| `-l`/`--file`     | flag  | Force the `<file_name>` argument to be a file id or name   |
| `-y`/`--yes`      | flag  | Confirm the prompt                                         |
| `-n`/`--no`       | flag  | Always deny the prompt                                     |


#### Arguments

| Argument    | Type  | nargs | Description                                    |
| :---------: | :---: | :---: | ---------------------------------------------- |
| `file_name` | `str` | >1    | The names of the file(s) to add into Vault     |
| `output`    | `str` | 1     | The output directory to decrypt the files into |

#### Output

The output will be colour coded - Successes will be in green, and errors will be in red. 

Successful output will look like this:

```sh
> vault file delete test_file.txt
Please Enter Your Password:

You are about to delete "test_file.txt". Deleting <files|groups|folders> is irreversable.
Would you like to continue? [y/N]: y

File test_file.txt deleted
```

Error conditions will look like this:

```sh
> vault file delete test_file.txt
Please Enter Your Password:

You are about to delete "test_file.txt". Deleting <files|groups|folders> is irreversable.
Would you like to continue? [y/N]: y

Error: File "<file_name>" not found
```

Error Messages:

- Error: File "<file_name>" not found
- Error: Cannot find group "<file_name>". Please remove the -g/--group flags to automatically search for a match.
- Error: Cannot find folder "<file_name>". Please remove the -f/--folder flags to automatically search for a match.
- Error: Cannot find output folder "<folder_name>"
- Error: Cannot create output folder "<folder_name>"

### 0.3 - `file rename <file_name> <new_file_name>`

This command will rename a file, group or folder. This will prompt the user for confirmation.

#### Options

| Option            | Type  | Description                                                |
| :---------------: | :---: | ---------------------------------------------------------- |
| `-p`/`--password` | `str` | The Vault master password                                  |
| `-d`/`--debug`    | flag  | Enable debug logging                                       |
| `-v`/`--vault`    | `str` | The vault name                                             |
| `-f`/`--folder`   | flag  | Force the `<file_name>` argument to be a folder id or name |
| `-l`/`--file`     | flag  | Force the `<file_name>` argument to be a file id or name   |
| `-y`/`--yes`      | flag  | Confirm the prompt                                         |
| `-n`/`--no`       | flag  | Always deny the prompt                                     |


#### Arguments

| Argument        | Type  | nargs | Description                                |
| :-------------: | :---: | :---: | ------------------------------------------ |
| `file_name`     | `str` | 1     | The names of the file(s) to add into Vault |
| `new_file_name` | `str` | 1     | The new file name to list this as          |

#### Output

The output will be colour coded - Successes will be in green, and errors will be in red. 

Successful output will look like this:

```sh
> vault file rename test_file.txt test_file_2.txt
Please Enter Your Password:

You are about to rename "test_file.txt" to "test_file_2.txt". Rename <files|groups|folders> is irreversable.
Would you like to continue? [y/N]: y

File "test_file.txt" renamed to "test_file_2.txt"
```

Error conditions will look like this:

```sh
> vault file rename test_file.txt test_file_2.txt
Please Enter Your Password:

You are about to rename "test_file.txt" to "test_file_2.txt". Rename <files|groups|folders> is irreversable.
Would you like to continue? [y/N]: y

Error: File "test_file.txt" not found
```

Error Messages:

- Error: File "<file_name>" not found
- Error: Cannot find group "<file_name>". Please remove the -g/--group flags to automatically search for a match.
- Error: Cannot find folder "<file_name>". Please remove the -f/--folder flags to automatically search for a match.
- Error: Cannot find output folder "<folder_name>"
- Error: Cannot create output folder "<folder_name>"


### 0.3 - `file replace <file_name> <filepath`

This command will replace a given file in a Vault with another file. This will overwrite the file with the new one, updating metadata and file contents. This will be an irreversable change.

#### Options

| Option            | Type  | Description                                                |
| :---------------: | :---: | ---------------------------------------------------------- |
| `-p`/`--password` | `str` | The Vault master password                                  |
| `-d`/`--debug`    | flag  | Enable debug logging                                       |
| `-v`/`--vault`    | `str` | The vault name                                             |
| `-f`/`--folder`   | flag  | Force the `<file_name>` argument to be a folder id or name |
| `-l`/`--file`     | flag  | Force the `<file_name>` argument to be a file id or name   |
| `-y`/`--yes`      | flag  | Confirm the prompt                                         |
| `-n`/`--no`       | flag  | Always deny the prompt                                     |


#### Arguments

| Argument    | Type  | nargs | Description                                          |
| :---------: | :---: | :---: | ---------------------------------------------------- |
| `file_name` | `str` | 1     | The names of the file(s) to add into Vault           |
| `filepath`  | `str` | >1    | The filepath of the new file to replace the old file |

#### Output

The output will be colour coded - Successes will be in green, and errors will be in red. 

Successful output will look like this:

```sh
> vault file replace test_file.txt ./test_file_2.txt
Please Enter Your Password:

You are about to rename "test_file.txt" to "test_file_2.txt". Rename <files|groups|folders> is irreversable.
Would you like to continue? [y/N]: y

File "test_file.txt" replaced by "test_file_2.txt"
```

Errors will look like this:

```sh
> vault file replace test_file.txt ./test_file_2.txt
Please Enter Your Password:

You are about to rename "test_file.txt" to "test_file_2.txt". Rename <files|groups|folders> is irreversable.
Would you like to continue? [y/N]: y

Error: File "test_file.txt" does not exist.
```

Error Messages:

- Error: File "<file_name>" not found
- Error: Cannot find group "<file_name>". Please remove the -g/--group flags to automatically search for a match.
- Error: Cannot find folder "<file_name>". Please remove the -f/--folder flags to automatically search for a match.
- Error: Cannot find output folder "<folder_name>"
- Error: Cannot create output folder "<folder_name>"

### 0.3 - `file show <file_name>`

This command will show a file, folder or group that is listed under the given IDs or names.

This will show the relevant information about a File, Group and Folders are in the output section.


#### Options

| Option            | Type  | Description                                                |
| :---------------: | :---: | ---------------------------------------------------------- |
| `-p`/`--password` | `str` | The Vault master password                                  |
| `-d`/`--debug`    | flag  | Enable debug logging                                       |
| `-v`/`--vault`    | `str` | The vault name                                             |
| `-f`/`--folder`   | flag  | Force the `<file_name>` argument to be a folder id or name |
| `-l`/`--file`     | flag  | Force the `<file_name>` argument to be a file id or name   |


#### Arguments

| Argument    | Type  | nargs | Description                                |
| :---------: | :---: | :---: | ------------------------------------------ |
| `file_name` | `str` | >1    | The names of the file(s) to add into Vault |

#### Output

The output will be colour coded - Successes will be in green, and errors will be in red. 

Successful output will look like this:

```sh
> vault file show test_file.txt
Please Enter Your Password:

File:             "test_file.txt"
UUID:             <file_uuid>
Groups:           <file_groups>
Mime:             <file_mime>
Extension:        <file_extension>
Created:          <vault_created>
Last Modified:    <vault_modified>
Size of File:     <file_size>
Unencrypted Hash: <file_hash>
Encrypted Hash:   <file_hash>

Group:       "Test File"
Group UUID:  <group_uuid>
Files:       <group_files>
Created:     <group_created>
Modified:    <group_modified>

Folder:      "Test Folder"
Folder UUID: <folder_uuid>
Files:       <folder_files>
Created:     <folder_created>
Modifief:    <folder_modified>
```

Errors will look like this:

```sh
> vault file show test_file.txt
Please Enter Your Password:

Error: File "test_file.txt" does not exist.
```

Error Messages:

- Error: File "<file_name>" not found
- Error: Cannot find group "<file_name>". Please remove the -g/--group flags to automatically search for a match.
- Error: Cannot find folder "<file_name>". Please remove the -f/--folder flags to automatically search for a match.
- Error: Cannot find output folder "<folder_name>"
- Error: Cannot create output folder "<folder_name>"

---

## Generate

### 0.1 - `generate password`

Generate a possible new master password.

#### Output

```sh
> vault generate password
<randomly_generated_password>
```

### 0.1 - `generate hash <hash_algorithm> <file_path>`

Take in a filepath or string, and create a hash algorithm, and hashes the file(s) and the string.

#### Arguments

| Argument         | Type     | Nargs | Description                    |
| :--------------: | :------: | :---: | ------------------------------ |
| `hash_algorithm` | `choice` | 1     | The hash algorithm to use      |
| `file_path`      | `str`    | >1    | The filepath or string to hash |

#### Output

The output of the hash algorithm

```sh
> vault generate hash md5 ./image.jpg
<file_hash>
```

### 0.1 - `generate encryption-key`

Generate a new random encryption key.

#### Output

```sh
> vault generate encryption-key
<new_encryption_key>
```

### 0.5 - `generate name`

### 0.1 - `generate uuid`

Generate a new UUID.

#### Output

```sh
> vault generate uuid
<new_uuid>
```

---

## Arbitrary Encryption and Decryption

### 0.4 - `encrypt <file_name>`

### 0.4 - `decrypt <file_name>`

---

## Versioning and Update

### 0.1 - `version`

This command will show the version of the program and exit.

#### Options

| Option         | Type  | Description           |
| :------------: | :---: | --------------------- |
| `-d`/`--debug` | flag` | Enable debug logging. |

#### Ouput

The default mode is the short mode, and the output will be in white.

```sh
> vault version 
Vault v0.1.0 
```

The long version will also be in white.

```sh
> vault version -d
Vault v0.1.0 - Python v3.9.0 for Windows 10.0.19041
```

### 0.4 - `update`

---

## PyPi Packages Needed

- click
- colorama
- pyyaml
- sqlalchemy
- cryptography
- https://github.com/dwyl/english-words