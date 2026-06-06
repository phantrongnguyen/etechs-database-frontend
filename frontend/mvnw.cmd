@REM ----------------------------------------------------------------------------
@REM Licensed to the Apache Software Foundation (ASF) under one
@REM or more contributor license agreements.  See the NOTICE file
@REM distributed with this work for additional information
@REM regarding copyright ownership.  The ASF licenses this file
@REM to you under the Apache License, Version 2.0 (the
@REM "License"); you may not use this file except in compliance
@REM with the License.  You may obtain a copy of the License at
@REM
@REM    https://www.apache.org/licenses/LICENSE-2.0
@REM
@REM Unless required by applicable law or agreed to in writing,
@REM software distributed under the License is distributed on an
@REM "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
@REM KIND, either express or implied.  See the License for the
@REM specific language governing permissions and limitations
@REM under the License.
@REM ----------------------------------------------------------------------------

@REM ----------------------------------------------------------------------------
@REM Maven Start Up Batch script
@REM
@REM Required ENV vars:
@REM JAVA_HOME - location of a JDK home dir
@REM
@REM Optional ENV vars
@REM M2_HOME - location of maven2's installed home dir
@REM MAVEN_BATCH_ECHO - set to 'on' to enable the echoing of the batch commands
@REM MAVEN_BATCH_PAUSE - set to 'on' to wait for a keystroke before ending
@REM MAVEN_OPTS - parameters passed to the Java VM when running Maven
@REM     e.g. to debug Maven itself, use
@REM set MAVEN_OPTS=-Xdebug -Xrunjdwp:transport=dt_socket,server=y,suspend=y,address=8000
@REM MAVEN_SKIP_RC - flag to disable loading of mavenrc files
@REM ----------------------------------------------------------------------------

@REM Begin all REM lines with '@' in case MAVEN_BATCH_ECHO is 'on'
@echo off
@REM set title of command window
title %0
@REM enable echoing by setting MAVEN_BATCH_ECHO to 'on'
@if "%MAVEN_BATCH_ECHO%" == "on"  echo %MAVEN_BATCH_ECHO%

@REM set %HOME% to equivalent of $HOME
if "%HOME%" == "" (set "HOME=%HOMEDRIVE%%HOMEPATH%")

@REM Execute a user defined script before this one
if not "%MAVEN_SKIP_RC%" == "" goto skipRcPre
@REM check for pre script, once with legacy .bat ending and once with .cmd ending
if exist "%USERPROFILE%\mavenrc_pre.bat" call "%USERPROFILE%\mavenrc_pre.bat" 2>nul
if exist "%USERPROFILE%\mavenrc_pre.cmd" call "%USERPROFILE%\mavenrc_pre.cmd" 2>nul
:skipRcPre

@setlocal

set "ERROR_CODE=0"

@REM To isolate internal variables from possible post scripts, we use another setlocal
@setlocal

@REM ==== START VALIDATION ====
if not "%JAVA_HOME%" == "" goto OkJHome

echo.
echo Error: JAVA_HOME not found in your environment. >&2
echo Please set the JAVA_HOME variable in your environment to match the >&2
echo location of your Java installation. >&2
echo.
goto error

:OkJHome
if exist "%JAVA_HOME%\bin\java.exe" goto init

echo.
echo Error: JAVA_HOME is set to an invalid directory. >&2
echo JAVA_HOME = "%JAVA_HOME%" >&2
echo Please set the JAVA_HOME variable in your environment to match the >&2
echo location of your Java installation. >&2
echo.
goto error

@REM ==== END VALIDATION ====

:init

@REM Find the project base dir, i.e. the directory that contains the folder ".mvn".
@REM Fallback to current working directory if not found.

set "MAVEN_PROJECTBASEDIR=%MAVEN_BASEDIR%"
if not "%MAVEN_PROJECTBASEDIR%"=="" goto endDetectBaseDir

set "EXEC_DIR=%CD%"
set "WDIR=%EXEC_DIR%"
@REM look for the --file switch and start the search for the --file switch name
set "WDIR=%CD%"
if not "%MAVEN_PROJECTBASEDIR%"=="" goto endDetectBaseDir

set "EXEC_DIR=%CD%"
set "WDIR=%EXEC_DIR%"

:searchBaseDir
@REM Find the project base dir
set "MAVEN_PROJECTBASEDIR=%WDIR%"
if exist "%MAVEN_PROJECTBASEDIR%\.mvn\jvm.config" goto endDetectBaseDir
if exist "%MAVEN_PROJECTBASEDIR%\.mvn\maven.config" goto endDetectBaseDir
if exist "%MAVEN_PROJECTBASEDIR%\.mvn\extensions" goto endDetectBaseDir

set "WDIR=%WDIR%"
if "%WDIR%"=="%CD%" goto baseDirNotFound
cd ..
set "WDIR=%CD%"
goto searchBaseDir

:baseDirNotFound
set "MAVEN_PROJECTBASEDIR=%EXEC_DIR%"
cd "%EXEC_DIR%"

:endDetectBaseDir

@REM JVM options are configured in pom.xml spring-boot-maven-plugin

@echo off

if "%OS%"=="Windows_NT" setlocal enabledelayedexpansion

set "MVNW_REPOURL=https://repo.maven.apache.org/maven2"
if defined MVNW_REPOURL (
  set "MVNW_REPOURL=%MVNW_REPOURL%/org/apache/maven/wrapper/maven-wrapper/3.3.2/maven-wrapper-3.3.2.jar"
)

set "MAVEN_JAR_EXE=%MAVEN_PROJECTBASEDIR%\.mvn\wrapper\maven-wrapper.jar"
if exist "%MAVEN_JAR_EXE%" goto runJar

echo.
echo Error: Could not find Maven wrapper JAR at "%MAVEN_JAR_EXE%". >&2
echo Downloading from: %MVNW_REPOURL% >&2
echo.
if exist "%TEMP%\maven-wrapper-3.3.2.jar" (
    echo Found cached copy in %%TEMP%%
    copy "%TEMP%\maven-wrapper-3.3.2.jar" "%MAVEN_JAR_EXE%"
)
if exist "%MAVEN_JAR_EXE%" goto runJar

echo Downloading Maven Wrapper JAR...
powershell -Command "Invoke-WebRequest -Uri '%MVNW_REPOURL%' -OutFile '%MAVEN_JAR_EXE%'" 2>nul

:runJar
@REM Execute Maven
"%JAVA_HOME%\bin\java.exe" %MAVEN_OPTS% -jar "%MAVEN_JAR_EXE%" %*

:error
set "ERROR_CODE=1"

:end
@exit /b %ERROR_CODE%
