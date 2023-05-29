using Azure.Identity;
using Kusto.Data.Common;
using Kusto.Data.Net.Client;
using Kusto.Data;
using System;
using System.Collections.Generic;
using System.Diagnostics.Metrics;
using System.Linq;
using System.Security.Policy;
using System.Text;
using System.Threading.Tasks;
using Kusto.Cloud.Platform.Data;
using System.IO;
using System.Text.Json;
using Iot.Core.DLL;

namespace Iot.Core.DAL
{
    public static class DALKusto
    {
        static KustoConnectionStringBuilder builder = new KustoConnectionStringBuilder("https://clusterserre.eastus2.kusto.windows.net/databaseserre");

        public static DLLTemperaturePourcentageDate GetDataTableauDeBord()
        {
            // Code de base
            //var client = Kusto.Data.Net.Client.KustoClientFactory.CreateCslQueryProvider(builder);
            //var query = $@"tableserre | count";
            //var reader = client.ExecuteQuery(query);

            //var array = reader.ToEnumerableObjectArray();

            //DLLTemperaturePourcentageDate dLLTemperatureDate = new DLLTemperaturePourcentageDate();

            //dLLTemperatureDate.lstTemperaturePourcentageDate = new List<DLLTemperaturePourcentageDateItem>();

            //foreach (var item in array)
            //{
            //    DLLTemperaturePourcentageDateItem dLLTemperaturePourcentageDateItem = new DLLTemperaturePourcentageDateItem();
            //    dLLTemperaturePourcentageDateItem.temperature = (float)item[0];
            //    dLLTemperaturePourcentageDateItem.date = (DateTime)item[3];
            //    dLLTemperaturePourcentageDateItem.pourcentage = (float)item[1];

            //    dLLTemperatureDate.lstTemperaturePourcentageDate.Add(dLLTemperaturePourcentageDateItem);

            //}

            //reader.Close();

            // s'il y a un problème technique
            string jsonString = File.ReadAllText(Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments) + "/donneesSimulees.json");

            DLLTemperaturePourcentageDate dLLTemperatureDate = JsonSerializer.Deserialize<DLLTemperaturePourcentageDate>(jsonString);

            return dLLTemperatureDate;
        }  

    }
}
