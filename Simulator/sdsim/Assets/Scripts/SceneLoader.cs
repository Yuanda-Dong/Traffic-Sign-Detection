using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using SimpleFileBrowser;
public class SceneLoader : MonoBehaviour {

public void LoadGenerateRoadScene()
{
    SceneManager.LoadSceneAsync(1);
}

public void LoadWarehouseScene()
{
    SceneManager.LoadSceneAsync(2);
}

public void LoadAVCScene()
{
    SceneManager.LoadSceneAsync(3);
}

public void LoadMenuScene()
{
    SceneManager.LoadSceneAsync(0);
}

public void LoadGeneratedTrackScene()
{
    SceneManager.LoadSceneAsync(4);
}

public void LoadRoboRacingLeague1Scene()
{
    SceneManager.LoadSceneAsync(6);
}

public void LoadTestTrackScene()
{
    SceneManager.LoadSceneAsync(7);
}

public void LoadTestTrack1Scene()
{
    SceneManager.LoadSceneAsync(8);
}

public void LoadTestTrack2Scene()
{
    SceneManager.LoadSceneAsync(9);
}

public void LoadMelbourneScene()
{
    SceneManager.LoadSceneAsync(10);
}

public void LoadShanghaiScene()
{
    SceneManager.LoadSceneAsync(11);
}

public void LoadTestTrack3Scene()
{
    SceneManager.LoadSceneAsync(12);
}

public void LoadTestTrack4Scene()
{
    SceneManager.LoadSceneAsync(13);
}

public void LoadSignMelbourneScene()
{
    SceneManager.LoadSceneAsync(14);
}

public void LoadSignShanghaiScene()
{
    SceneManager.LoadSceneAsync(15);
}

public void QuitApplication()
{
    Application.Quit();
}

public void SetLogDir()
{
    // Show a select folder dialog 
    // onSuccess event: print the selected folder's path
    // onCancel event: print "Canceled"
    // Load file/folder: folder, Initial path: default (Documents), Title: "Select Folder", submit button text: "Select"
     FileBrowser.ShowLoadDialog( (path) => { OnSetLogDir(path); }, 
                                    () => { Debug.Log( "Canceled" ); }, 
                                    true, null, "Select Log Folder", "Select" );
}

public void OnSetLogDir(string path)
{
    Debug.Log( "Selected: " + path );
    GlobalState.log_path = path;
}

}
