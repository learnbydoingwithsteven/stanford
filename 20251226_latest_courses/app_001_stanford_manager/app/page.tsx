"use client";

import { useState, useEffect } from "react";
import { BookOpen, Video, FileText, Search, BarChart2, Folder, ExternalLink } from "lucide-react";
import { motion } from "framer-motion";

export default function Home() {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/api/courses")
      .then((res) => res.json())
      .then((data) => {
        setCourses(data);
        setLoading(false);
      })
      .catch((err) => console.error(err));
  }, []);

  if (loading) return <div className="flex h-screen items-center justify-center bg-gray-950 text-white">Loading Local Knowledge Base...</div>;

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100 font-sans selection:bg-blue-500/30">
      {/* Header */}
      <header className="border-b border-gray-800 bg-gray-900/50 backdrop-blur-xl sticky top-0 z-50">
        <div className="container mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-blue-500/20">
              <BookOpen className="text-white w-6 h-6" />
            </div>
            <div>
               <h1 className="text-xl font-bold tracking-tight">Stanford AI <span className="text-blue-400">Hub</span></h1>
               <p className="text-xs text-gray-400">Local Knowledge Manager</p>
            </div>
          </div>
          
          <div className="flex items-center gap-4">
             <div className="relative group">
                <Search className="absolute left-3 top-2.5 w-4 h-4 text-gray-500 group-focus-within:text-blue-400 transition-colors" />
                <input 
                  type="text" 
                  placeholder="Search concepts, lectures..." 
                  className="bg-gray-900 border border-gray-800 rounded-full py-2 pl-10 pr-4 text-sm focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all w-64 focus:w-80"
                />
             </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-10">
        
        {/* Stats / Hero */}
        <section className="mb-12">
           <motion.div 
             initial={{ opacity: 0, y: 20 }}
             animate={{ opacity: 1, y: 0 }}
             transition={{ duration: 0.5 }}
             className="grid grid-cols-1 md:grid-cols-4 gap-6"
           >
              <div className="bg-gradient-to-br from-indigo-900/20 to-blue-900/10 border border-indigo-500/20 p-6 rounded-2xl relative overflow-hidden group">
                  <div className="absolute top-0 right-0 w-24 h-24 bg-indigo-500/10 rounded-full blur-2xl -mr-10 -mt-10 transition-transform group-hover:scale-150"></div>
                  <h3 className="text-indigo-400 text-sm font-medium mb-1">Total Courses</h3>
                  <p className="text-3xl font-bold">{courses.length}</p>
              </div>
               <div className="bg-gray-900/50 border border-gray-800 p-6 rounded-2xl">
                  <h3 className="text-gray-400 text-sm font-medium mb-1">Total Lectures</h3>
                  <p className="text-3xl font-bold white">{courses.reduce((acc, c) => acc + c.lectures.length, 0)}</p>
              </div>
              <div className="bg-gray-900/50 border border-gray-800 p-6 rounded-2xl">
                  <h3 className="text-gray-400 text-sm font-medium mb-1">Knowledge Nodes</h3>
                  <p className="text-3xl font-bold text-emerald-400">~{courses.reduce((acc, c) => acc + c.lectures.length, 0) * 5}</p>
              </div>
               <div className="bg-gray-900/50 border border-gray-800 p-6 rounded-2xl flex items-center justify-center cursor-pointer hover:bg-gray-800 transition-colors group">
                  <div className="text-center">
                    <BarChart2 className="w-8 h-8 mx-auto mb-2 text-gray-500 group-hover:text-amber-400 transition-colors" />
                    <span className="text-sm text-gray-400">View Knowledge Graph</span>
                  </div>
              </div>
           </motion.div>
        </section>

        {/* Course Grid */}
        <h2 className="text-2xl font-semibold mb-6 flex items-center gap-2">
            <span className="w-1 h-8 bg-blue-500 rounded-full inline-block"></span>
            My Courses
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
           {courses.map((course, idx) => (
             <motion.div 
               key={course.id}
               initial={{ opacity: 0, scale: 0.95 }}
               animate={{ opacity: 1, scale: 1 }}
               transition={{ delay: idx * 0.1 }}
               className="bg-gray-900 border border-gray-800 rounded-2xl overflow-hidden hover:border-gray-700 hover:shadow-2xl hover:shadow-black/50 transition-all group"
             >
                <div className="h-32 bg-gray-800/50 relative overflow-hidden">
                   {/* Placeholder Gradient based on course ID hash or simply generic */}
                   <div className={`absolute inset-0 opacity-40 bg-gradient-to-r ${idx % 2 === 0 ? 'from-blue-600 to-indigo-600' : 'from-emerald-600 to-teal-600'}`}></div>
                   <div className="absolute bottom-4 left-6">
                      <span className="bg-black/60 backdrop-blur-md text-xs font-mono px-2 py-1 rounded border border-white/10 text-white/80">{course.id}</span>
                   </div>
                </div>
                
                <div className="p-6">
                   <div className="flex justify-between items-start mb-4">
                      <h3 className="text-xl font-bold group-hover:text-blue-400 transition-colors">{course.title}</h3>
                   </div>
                   
                   <p className="text-gray-400 text-sm mb-6 line-clamp-2">
                      {course.lectures.length} Lectures • {course.playlist_url ? 'Video Playlist Available' : 'No Video Playlist'}
                   </p>
                   
                   <div className="space-y-3">
                      {course.lectures.slice(0, 3).map((lec, i) => (
                        <div key={i} className="flex items-center gap-3 text-sm text-gray-300 hover:bg-gray-800 p-2 rounded-lg cursor-pointer transition-colors">
                           <FileText className="w-4 h-4 text-gray-500" />
                           <span className="truncate flex-1">{lec.title}</span>
                           {lec.materials.some(m => m.type === 'slides') && <span className="text-[10px] bg-blue-500/20 text-blue-300 px-1.5 py-0.5 rounded">PDF</span>}
                        </div>
                      ))}
                      {course.lectures.length > 3 && (
                        <div className="text-center pt-2">
                           <span className="text-xs text-gray-500 font-medium hover:text-gray-300 cursor-pointer">+{course.lectures.length - 3} more lectures</span>
                        </div>
                      )}
                   </div>
                   
                   <div className="mt-6 flex items-center justify-between pt-4 border-t border-gray-800">
                      <a href={`/course/${course.id}`} className="text-sm font-medium text-white hover:text-blue-400 transition-colors flex items-center gap-1">
                        Open Course <ExternalLink className="w-3 h-3" />
                      </a>
                      
                      {course.playlist_url && (
                        <a href={course.playlist_url} target="_blank" rel="noreferrer" className="text-gray-500 hover:text-red-400 transition-colors">
                           <Video className="w-5 h-5" />
                        </a>
                      )}
                   </div>
                </div>
             </motion.div>
           ))}
        </div>
      </main>
    </div>
  );
}
