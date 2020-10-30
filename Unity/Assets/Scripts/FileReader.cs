using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

public class FileReader
{
    public static List<(double, double)> read()
    {
        string[] lines = File.ReadAllLines(@"C:\Users\Isbla\dirs\Assets\Scripts\0file_dir_continuous.txt");
        List<string[]> mod_lines = new List<string[]>();
        List<(double, double)> dirs = new List<(double, double)>();

        string sep = "\t";
        double prev = 0;
        foreach (string line in lines)
        {
            mod_lines.Add(line.Split(sep.ToCharArray()));
        }
        foreach (var array in mod_lines)
        {
            double dir = 0;
            float dist = 0;
            foreach (var item in array)
            {
                if (item.Contains(','))
                {
                    string[] separated = item.Split(',');
                    dir = float.Parse(separated[0].ToString());
                    if (dir > 180)
                    {
                        dir = -360 + dir;
                    }
                    dir = 180 - dir;
                    prev = dir;
                }
                if (item.Contains('F') || item.Contains("F"))
                {
                    int ind = Array.IndexOf(array, item);
                    dist = (float) (float.Parse(array[ind + 1].ToString())) * 29 * 0.82f;
                    dir = prev;
                }
                if (item == "None")
                {
                    dir = prev;
                }

            }
            dirs.Add((dist, dir));
        }
        return dirs;
    }
}