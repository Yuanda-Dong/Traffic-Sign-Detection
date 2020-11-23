using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net;
using System.Net.Sockets;
using System;
using UnityEngine.UI;
using System.Globalization;

namespace tk
{
    
    public class TcpMenuHandler : MonoBehaviour {

        public SceneLoader loader;
        private tk.JsonTcpClient client;

        public void Init(tk.JsonTcpClient _client)
        {
            _client.dispatchInMainThread = true;

            client = _client;
            client.dispatcher.Register("load_scene", new tk.Delegates.OnMsgRecv(OnLoadScene));
            client.dispatcher.Register("get_protocol_version", new tk.Delegates.OnMsgRecv(OnProtocolVersion));
            client.dispatcher.Register("get_scene_names", new tk.Delegates.OnMsgRecv(OnGetSceneNames));
            client.dispatcher.Register("quit_app", new tk.Delegates.OnMsgRecv(OnQuitApp));
            client.dispatcher.Register("connected", new tk.Delegates.OnMsgRecv(OnConnected));
        }

        public void Start()
        {
        }

        public void OnDestroy()
        {
            if(client)
                client.dispatcher.Reset();
        }

        void Disconnect()
        {
            client.Disconnect();
        }
      
        void OnProtocolVersion(JSONObject msg)
        {
            JSONObject json = new JSONObject(JSONObject.Type.OBJECT);
            json.AddField("msg_type", "protocol_version");
            json.AddField("version", "2");
            
            client.SendMsg( json );
        }

        void OnConnected(JSONObject msg)
        {
            SendFELoaded();
        }

        private void SendFELoaded()
        {
            JSONObject json = new JSONObject(JSONObject.Type.OBJECT);
            json.AddField("msg_type", "scene_selection_ready");
            json.AddField("loaded", "1");        

            client.SendMsg( json );
        }

        void OnGetSceneNames(JSONObject jsonObject)
        {
            SendSceneNames();
        }

        private void SendSceneNames()
        {
            JSONObject scenes = new JSONObject(JSONObject.Type.ARRAY);

            scenes.Add("generated_road");
            scenes.Add("warehouse");
            scenes.Add("sparkfun_avc");
            scenes.Add("generated_track");
            scenes.Add("roboracingleague_1");
            scenes.Add("test_track");
            scenes.Add("test_track_1");
            scenes.Add("test_track_2");
            scenes.Add("f1_melbourne");
            scenes.Add("f1_shanghai");
            scenes.Add("test_track_3");
            scenes.Add("test_track_4");
            scenes.Add("sign_melbourne");
            scenes.Add("sign_shanghai");

            JSONObject json = new JSONObject(JSONObject.Type.OBJECT);
            json.AddField("scene_names", scenes);
            json.AddField("msg_type", "scene_names");

            client.SendMsg( json );
        }

        void OnLoadScene(JSONObject jsonObject)
        {
            GlobalState.bAutoHideSceneMenu = true;

            // since we know this is called only from a network client,
            // we can also infer that we don't want to auto create 
            GlobalState.bCreateCarWithoutNetworkClient = false;

            string scene_name = jsonObject.GetField("scene_name").str;

            if(scene_name == "generated_road")
            {
                loader.LoadGenerateRoadScene();
            }
            else if (scene_name == "warehouse")
            {
                loader.LoadWarehouseScene();
            }
            else if (scene_name == "sparkfun_avc")
            {
                loader.LoadAVCScene();
            }
            else if (scene_name == "generated_track")
            {
                loader.LoadGeneratedTrackScene();
            }
            else if (scene_name == "roboracingleague_1")
            {
                loader.LoadRoboRacingLeague1Scene();
            }
            else if (scene_name == "test_track")
            {
                loader.LoadTestTrackScene();
            }
            else if (scene_name == "test_track_1")
            {
                loader.LoadTestTrack1Scene();
            }
            else if (scene_name == "test_track_2")
            {
                loader.LoadTestTrack2Scene();
            }
            else if (scene_name == "f1_melbourne")
            {
                loader.LoadMelbourneScene();
            }
            else if (scene_name == "f1_shanghai")
            {
                loader.LoadShanghaiScene();
            }
            else if (scene_name == "test_track_3")
            {
                loader.LoadTestTrack3Scene();
            }
            else if (scene_name == "test_track_4")
            {
                loader.LoadTestTrack4Scene();
            }
            else if (scene_name == "sign_melbourne")
            {
                loader.LoadSignMelbourneScene();
            }
            else if (scene_name == "sign_shanghai")
            {
                loader.LoadSignShanghaiScene();
            }
        }
        
        void OnQuitApp(JSONObject json)
        {
            Application.Quit();
        }        
    }
}
