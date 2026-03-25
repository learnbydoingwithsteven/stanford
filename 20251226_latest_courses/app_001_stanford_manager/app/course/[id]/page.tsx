"use client";

import { useState, useEffect, use } from "react";
import { ArrowLeft, BookOpen, FileText, Video, Monitor, Download, ExternalLink } from "lucide-react";
import Link from "next/link";
import { motion } from "framer-motion";

export default function CoursePage({ params }: { params: Promise<{ id: string }> }) {
    const resolvedParams = use(params);
    const { id } = resolvedParams;
    const [course, setCourse] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [selectedLecture, setSelectedLecture] = useState<any>(null);

    useEffect(() => {
        fetch(`http://localhost:8000/api/courses/${id}`)
            .then((res) => res.json())
            .then((data) => {
                setCourse(data);
                if (data.lectures && data.lectures.length > 0) {
                    setSelectedLecture(data.lectures[0]);
                }
                setLoading(false);
            })
            .catch((err) => console.error(err));
    }, [id]);

    const getLocalUrl = (lecture: any, type: string) => {
        // Find the material of this type
        const mat = lecture.materials.find((m: any) => m.type === type);
        if (!mat) return null;

        // Calculate filename from URL
        const filename = mat.url.split('/').pop().split('?')[0];
        // If it doesn't end in pdf and is notes, it might be notes.md. The downloader handles this.
        // For now, let's assume PDF if content-type matches or check URL.

        return `http://localhost:8000/api/files/${id}/${lecture.local_dir}/${filename}`;
    };

    if (loading) return <div className="flex h-screen items-center justify-center bg-gray-950 text-white">Loading Course Data...</div>;

    if (!course) return <div className="flex h-screen items-center justify-center bg-gray-950 text-red-400">Course Not Found</div>;

    return (
        <div className="min-h-screen bg-gray-950 text-gray-100 flex flex-col h-screen overflow-hidden">
            {/* Header */}
            <header className="border-b border-gray-800 bg-gray-900 flex items-center justify-between px-6 py-4 shrink-0">
                <div className="flex items-center gap-4">
                    <Link href="/" className="p-2 hover:bg-gray-800 rounded-full transition-colors text-gray-400 hover:text-white">
                        <ArrowLeft className="w-5 h-5" />
                    </Link>
                    <div>
                        <h1 className="text-lg font-bold flex items-center gap-2">
                            <span className="text-blue-400">{course.id}</span>
                            <span className="text-gray-600">/</span>
                            <span>{course.title}</span>
                        </h1>
                    </div>
                </div>

                <div className="flex items-center gap-3">
                    {course.playlist_url && (
                        <a href={course.playlist_url} target="_blank" rel="noreferrer" className="flex items-center gap-2 px-3 py-1.5 bg-red-500/10 text-red-500 rounded-full text-xs font-medium hover:bg-red-500/20 transition-colors border border-red-500/20">
                            <Video className="w-3 h-3" /> YouTube Playlist
                        </a>
                    )}
                </div>
            </header>

            <div className="flex flex-1 overflow-hidden">
                {/* Sidebar List */}
                <aside className="w-80 border-r border-gray-800 bg-gray-900/50 flex flex-col overflow-hidden">
                    <div className="p-4 border-b border-gray-800">
                        <h2 className="text-xs font-semibold text-gray-400 uppercase tracking-wider">Lectures ({course.lectures.length})</h2>
                    </div>
                    <div className="flex-1 overflow-y-auto p-2 space-y-1">
                        {course.lectures.map((lec: any, i: number) => (
                            <button
                                key={i}
                                onClick={() => setSelectedLecture(lec)}
                                className={`w-full text-left p-3 rounded-lg text-sm transition-all flex items-start gap-3 ${selectedLecture?.title === lec.title ? 'bg-blue-600/20 text-blue-100 border border-blue-500/30' : 'text-gray-400 hover:bg-gray-800 hover:text-gray-200'}`}
                            >
                                <div className="mt-0.5 min-w-[16px]">
                                    {selectedLecture?.title === lec.title ? <div className="w-1.5 h-1.5 rounded-full bg-blue-400 mt-1.5"></div> : <span className="text-xs font-mono text-gray-600">{(i + 1).toString().padStart(2, '0')}</span>}
                                </div>
                                <span className="line-clamp-2">{lec.title}</span>
                            </button>
                        ))}
                    </div>
                </aside>

                {/* Main View Area */}
                <main className="flex-1 bg-gray-950 flex flex-col min-w-0">
                    {selectedLecture ? (
                        <div className="flex-1 flex flex-col h-full">
                            {/* Lecture Meta */}
                            <div className="p-6 border-b border-gray-800 bg-gray-900/20 shrink-0">
                                <motion.h2
                                    initial={{ opacity: 0, x: -10 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    className="text-2xl font-bold mb-4"
                                >
                                    {selectedLecture.title}
                                </motion.h2>

                                <div className="flex flex-wrap gap-4">
                                    {selectedLecture.materials.map((mat: any, idx: number) => {
                                        const localUrl = getLocalUrl(selectedLecture, mat.type);
                                        return (
                                            <div key={idx} className="flex flex-col gap-2">
                                                <div className="flex gap-2">
                                                    {localUrl && (
                                                        <a
                                                            href={localUrl}
                                                            target="_blank"
                                                            // rel="noopener noreferrer" // For now, let it open in new tab. Or iframe it below.
                                                            className="flex items-center gap-2 px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg hover:bg-gray-700 transition-colors text-sm font-medium"
                                                        >
                                                            {mat.type === 'slides' ? <Monitor className="w-4 h-4 text-purple-400" /> : <FileText className="w-4 h-4 text-emerald-400" />}
                                                            View Local {mat.type === 'slides' ? 'Slides' : 'Notes'}
                                                        </a>
                                                    )}
                                                    <a
                                                        href={mat.url}
                                                        target="_blank"
                                                        rel="noreferrer"
                                                        className="flex items-center gap-2 px-3 py-2 bg-gray-800/50 border border-gray-700/50 rounded-lg hover:bg-gray-800 transition-colors text-gray-400 text-sm hover:text-white"
                                                        title="Original Source"
                                                    >
                                                        <ExternalLink className="w-3 h-3" />
                                                    </a>
                                                </div>
                                            </div>
                                        );
                                    })}
                                </div>
                            </div>

                            {/* Preview Area (Iframe) */}
                            <div className="flex-1 bg-black/20 p-6 overflow-hidden flex flex-col">
                                {selectedLecture.materials.find((m: any) => m.type === 'slides') ? (
                                    <div className="flex-1 border border-gray-800 rounded-xl overflow-hidden bg-gray-900 relative">
                                        <iframe
                                            src={getLocalUrl(selectedLecture, 'slides') || ''}
                                            className="w-full h-full"
                                            title="PDF Preview"
                                        />
                                    </div>
                                ) : (
                                    <div className="flex-1 flex items-center justify-center text-gray-500 border border-dashed border-gray-800 rounded-xl">
                                        <div className="text-center">
                                            <FileText className="w-12 h-12 mx-auto mb-4 opacity-20" />
                                            <p>No preview available for slides.</p>
                                            <p className="text-sm">Check notes or external links.</p>
                                        </div>
                                    </div>
                                )}
                            </div>
                        </div>
                    ) : (
                        <div className="flex-1 flex items-center justify-center text-gray-500">
                            Select a lecture to view details
                        </div>
                    )}
                </main>

                {/* Knowledge Graph / Summary Panel (Placeholder) */}
                <aside className="w-80 border-l border-gray-800 bg-gray-900/30 p-4 hidden xl:block">
                    <h3 className="text-sm font-semibold text-gray-400 mb-4 uppercase tracking-wider flex items-center gap-2">
                        <BookOpen className="w-4 h-4" /> AI Summary
                    </h3>
                    <div className="bg-gray-800/50 rounded-xl p-4 text-sm text-gray-400 leading-relaxed mb-6">
                        <p>Select a lecture to see AI-generated summaries and key takeaways here. (Integration pending)</p>
                    </div>

                    <h3 className="text-sm font-semibold text-gray-400 mb-4 uppercase tracking-wider flex items-center gap-2">
                        <ExternalLink className="w-4 h-4" /> Related Concepts
                    </h3>
                    <div className="flex flex-wrap gap-2">
                        {['Transformers', 'Zero-shot', 'Attention', 'Backprop', 'Loss Function'].map(tag => (
                            <span key={tag} className="px-2 py-1 bg-blue-500/10 text-blue-400 rounded text-xs border border-blue-500/20">{tag}</span>
                        ))}
                    </div>
                </aside>
            </div>
        </div>
    );
}
