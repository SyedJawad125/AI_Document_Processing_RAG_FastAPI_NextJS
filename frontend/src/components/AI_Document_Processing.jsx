'use client';
import React, { useState, useEffect, useRef, useCallback } from 'react';
import AxiosInstance from "@/components/AxiosInstance";

/* ─── Global styles - Luxury Edition ─── */
const GLOBAL_CSS = `
  @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400;1,500;1,600;1,700&family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,300;1,400;1,500;1,600;1,700;1,800&family=JetBrains+Mono:wght@300;400;500;700&display=swap');

  *, *::before, *::after { box-sizing: border-box; }

  :root {
    --cream:     #faf8f5;
    --cream-dark: #e8e4dd;
    --pure-white: #ffffff;
    --ivory:     #f5f0e8;
    --gold:      #d4af37;
    --gold-light: #e8c96e;
    --gold-dark:  #b8941f;
    --platinum:  #e5e4e2;
    --charcoal:  #1a1a1a;
    --dark-charcoal: #0d0d0d;
    --surface:   #1e1e1e;
    --surface-2: #2a2a2a;
    --border:    #333333;
    --border-light: #404040;
    --text-primary: #ffffff;
    --text-secondary: #b0b0b0;
    --text-muted: #7a7a7a;
    --emerald:   #10b981;
    --sapphire:  #3b82f6;
    --ruby:      #ef4444;
    --amber:     #f59e0b;
    --violet:    #8b5cf6;
  }

  body { background: var(--charcoal); }
  .font-serif { font-family: 'Cormorant Garamond', Georgia, serif; }
  .font-sans  { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
  .font-mono  { font-family: 'JetBrains Mono', monospace; }

  ::-webkit-scrollbar { width: 3px; height: 3px; }
  ::-webkit-scrollbar-track { background: var(--surface); }
  ::-webkit-scrollbar-thumb { background: var(--gold); border-radius: 3px; }

  @keyframes fadeUp  { from{opacity:0;transform:translateY(20px)} to{opacity:1;transform:translateY(0)} }
  @keyframes fadeIn  { from{opacity:0} to{opacity:1} }
  @keyframes spinCW  { to{transform:rotate(360deg)} }
  @keyframes pulse   { 0%,100%{opacity:1} 50%{opacity:.5} }
  @keyframes shimmer { 0%{background-position:-200% 0} 100%{background-position:200% 0} }
  @keyframes goldPulse{ 0%,100%{border-color:var(--gold); box-shadow:0 0 0 0 rgba(212,175,55,0.2)} 50%{border-color:var(--gold-light); box-shadow:0 0 0 4px rgba(212,175,55,0.4)} }

  .anim-fade-up { animation:fadeUp .4s cubic-bezier(0.2,0.8,0.4,1) forwards; }
  .anim-fade-in { animation:fadeIn .3s ease forwards; }
  .anim-spin    { animation:spinCW .7s linear infinite; }
  .anim-pulse   { animation:pulse 2s ease infinite; }

  .luxury-card {
    background: linear-gradient(135deg, var(--surface) 0%, #181818 100%);
    border: 1px solid var(--border);
    backdrop-filter: blur(10px);
    transition: all 0.3s cubic-bezier(0.2,0.8,0.4,1);
  }
  .luxury-card:hover {
    border-color: var(--gold);
    transform: translateY(-2px);
    box-shadow: 0 20px 40px -20px rgba(0,0,0,0.5);
  }

  .gold-text {
    background: linear-gradient(135deg, var(--gold-light) 0%, var(--gold) 50%, var(--gold-dark) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  /* Pure White Buttons */
  .btn-white {
    background: var(--pure-white);
    color: var(--charcoal);
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    letter-spacing: 0.02em;
    font-size: 0.75rem;
    text-transform: uppercase;
    border: none;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    transition: all 0.2s ease;
    padding: 12px 28px;
    border-radius: 0;
  }

  .btn-white::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(0,0,0,0.05), transparent);
    transition: left 0.5s ease;
  }

  .btn-white:hover::before { left: 100%; }
  .btn-white:hover {
    background: var(--cream);
    transform: translateY(-1px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.15);
  }
  .btn-white:active { transform: translateY(0); }
  .btn-white:disabled {
    background: var(--text-muted);
    cursor: not-allowed;
    transform: none;
    opacity: 0.5;
  }

  /* Ghost Button */
  .btn-ghost {
    background: transparent;
    color: var(--text-secondary);
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 0.7rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    border: 1px solid var(--border);
    cursor: pointer;
    transition: all 0.2s;
    padding: 10px 20px;
  }
  .btn-ghost:hover {
    border-color: var(--gold);
    color: var(--gold);
    background: rgba(212,175,55,0.05);
  }

  .btn-danger {
    background: transparent;
    color: var(--ruby);
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 0.7rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    border: 1px solid rgba(239,68,68,0.3);
    cursor: pointer;
    transition: all 0.2s;
    padding: 10px 20px;
  }
  .btn-danger:hover {
    border-color: var(--ruby);
    background: rgba(239,68,68,0.1);
    color: var(--ruby);
  }

  /* Form Inputs */
  .inp {
    background: var(--surface-2);
    border: 1px solid var(--border);
    color: var(--text-primary);
    font-family: 'Inter', sans-serif;
    font-size: 0.85rem;
    outline: none;
    transition: all 0.2s;
    width: 100%;
    padding: 12px 16px;
  }
  .inp:focus {
    border-color: var(--gold);
    box-shadow: 0 0 0 3px rgba(212,175,55,0.1);
  }
  .inp::placeholder { color: var(--text-muted); }

  select.inp {
    cursor: pointer;
    appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%23d4af37' d='M6 8L1 3h10z'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 16px center;
  }

  .sect-label {
    font-family: 'Inter', sans-serif;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--gold);
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 20px;
    font-weight: 600;
  }
  .sect-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, var(--gold), transparent);
  }

  .badge {
    font-family: 'Inter', sans-serif;
    font-size: 0.65rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 4px 10px;
    border: 1px solid;
    display: inline-flex;
    align-items: center;
    white-space: nowrap;
    font-weight: 600;
  }

  .tab-btn {
    font-family: 'Inter', sans-serif;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 16px 24px;
    background: transparent;
    border: none;
    border-bottom: 2px solid transparent;
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.2s;
    white-space: nowrap;
  }
  .tab-btn:hover { color: var(--text-primary); }
  .tab-btn.active {
    color: var(--gold);
    border-bottom-color: var(--gold);
  }

  .stat-card {
    background: var(--surface);
    border: 1px solid var(--border);
    padding: 20px 24px;
    display: flex;
    flex-direction: column;
    gap: 6px;
    position: relative;
    overflow: hidden;
    transition: all 0.2s;
  }
  .stat-card:hover {
    border-color: var(--gold);
    transform: translateY(-1px);
  }

  .prog-bar { height: 2px; background: var(--surface-2); overflow: hidden; border-radius: 2px; }
  .prog-fill {
    height: 100%;
    background: var(--gold);
    transition: width 0.3s;
  }

  .h-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
  .h-dot.ok  { background: var(--emerald); box-shadow: 0 0 8px var(--emerald); }
  .h-dot.err { background: var(--ruby);    box-shadow: 0 0 8px var(--ruby); }
  .h-dot.unk { background: var(--text-muted); }
  .h-dot.proc { background: var(--amber);   box-shadow: 0 0 8px var(--amber); }

  .toast {
    font-family: 'Inter', sans-serif;
    font-size: 0.8rem;
    padding: 12px 20px;
    display: flex;
    align-items: center;
    gap: 12px;
    border-left: 3px solid;
    animation: fadeUp 0.25s ease;
    min-width: 260px;
    max-width: 380px;
    backdrop-filter: blur(10px);
  }

  hr {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 20px 0;
  }
`;

/* ─── Toast ─── */
let _setToasts = null;
const toast = {
  _push(type, msg) {
    const id = Date.now();
    _setToasts?.(p => [...p, { id, type, msg }]);
    setTimeout(() => _setToasts?.(p => p.filter(t => t.id !== id)), 4000);
  },
  success: m => toast._push('success', m),
  error:   m => toast._push('error', m),
  warn:    m => toast._push('warn', m),
  info:    m => toast._push('info', m),
};
const TOAST_CFG = {
  success: { bg:'rgba(16,185,129,0.1)', border:'#10b981', color:'#10b981', icon:'✓' },
  error:   { bg:'rgba(239,68,68,0.1)', border:'#ef4444', color:'#ef4444', icon:'✕' },
  warn:    { bg:'rgba(245,158,11,0.1)', border:'#f59e0b', color:'#f59e0b', icon:'!' },
  info:    { bg:'rgba(59,130,246,0.1)', border:'#3b82f6', color:'#3b82f6', icon:'i' },
};
function Toasts() {
  const [toasts, setToasts] = useState([]);
  useEffect(() => { _setToasts = setToasts; }, []);
  return (
    <div style={{ position:'fixed', bottom:24, right:24, zIndex:9999, display:'flex', flexDirection:'column', gap:12, pointerEvents:'none' }}>
      {toasts.map(t => {
        const c = TOAST_CFG[t.type];
        return <div key={t.id} className="toast" style={{ background:c.bg, borderLeftColor:c.border, color:c.color, backdropFilter:'blur(10px)' }}>
          <span style={{ fontWeight:800, fontSize:'1rem' }}>{c.icon}</span> 
          <span style={{ fontWeight:500 }}>{t.msg}</span>
        </div>;
      })}
    </div>
  );
}

/* ─── Helpers ─── */
const fmt = {
  bytes: b => { if (!b) return '0 B'; const k=1024,s=['B','KB','MB','GB'],i=Math.floor(Math.log(b)/Math.log(k)); return (b/k**i).toFixed(1)+' '+s[i]; },
  date:  d => d ? new Date(d).toLocaleString() : '—',
  cut:   (s,n=80) => s && s.length>n ? s.slice(0,n)+'…' : (s||''),
};

/* ─── UI Primitives ─── */
function SectLabel({ children }) {
  return <div className="sect-label">{children}</div>;
}
function Badge({ children, color, gold }) {
  const style = gold
    ? { borderColor:'var(--gold)', color:'var(--gold)', background:'rgba(212,175,55,0.1)' }
    : { borderColor:`${color}40`, color, background:`${color}10` };
  return <span className="badge" style={style}>{children}</span>;
}
function Card({ children, style={}, className='' }) {
  return <div className={`luxury-card ${className}`} style={{ padding:24, ...style }}>{children}</div>;
}
function WhiteBtn({ children, loading, loadText='Processing…', style={}, ...props }) {
  return (
    <button className="btn-white" style={{ ...style }} {...props}>
      {loading ? (
        <span style={{ display:'flex', alignItems:'center', gap:8, justifyContent:'center' }}>
          <span className="anim-spin" style={{ width:14, height:14, border:'2px solid rgba(0,0,0,0.2)', borderTop:'2px solid #000', borderRadius:'50%', display:'inline-block' }} />
          {loadText}
        </span>
      ) : children}
    </button>
  );
}
function HDot({ status }) {
  const cls = status==='ready' ? 'ok' : status==='processing' ? 'proc' : status==='error' ? 'err' : 'unk';
  return <span className={`h-dot ${cls}`} />;
}

/* ═══════════════════════════════════ MAIN ═══════════════════════════════════ */
export default function AIDocumentProcessing() {
  const [mounted, setMounted] = useState(false);
  const [tab, setTab] = useState('documents');
  const [loading, setLoading] = useState(false);

  /* Documents */
  const [documents, setDocuments] = useState([]);
  const [selectedDoc, setSelectedDoc] = useState(null);
  const [docStatus, setDocStatus] = useState({});

  /* Upload */
  const [file, setFile] = useState(null);
  const [uploadPct, setUploadPct] = useState(0);
  const [dragging, setDragging] = useState(false);
  const fileRef = useRef();

  /* Chat */
  const [queryText, setQueryText] = useState('');
  const [chatMode, setChatMode] = useState('auto');
  const [topK, setTopK] = useState(5);
  const [chatHistory, setChatHistory] = useState([]);
  const [chatResult, setChatResult] = useState(null);

  /* Search */
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);

  /* Extraction */
  const [extractionFields, setExtractionFields] = useState('');
  const [extractionResult, setExtractionResult] = useState(null);

  /* Summary */
  const [summaryResult, setSummaryResult] = useState(null);

  /* ─ Init ─ */
  useEffect(() => {
    setMounted(true);
    fetchDocuments();
  }, []);

  /* ─── API Functions ─── */
  const fetchDocuments = async () => {
    try {
      const r = await AxiosInstance.get('/api/v1/documents/');
      setDocuments(r.data.data || []);
    } catch(e) {
      console.error('Error fetching documents:', e);
      toast.error('Failed to fetch documents');
    }
  };

  const checkDocumentStatus = async (docId) => {
    try {
      const r = await AxiosInstance.get(`/api/v1/documents/${docId}/status`);
      setDocStatus(prev => ({ ...prev, [docId]: r.data.data }));
      return r.data.data;
    } catch(e) {
      console.error('Error checking document status:', e);
      return null;
    }
  };

  const uploadDocument = async () => {
    if (!file) { toast.warn('Select a file first'); return; }
    const fd = new FormData();
    fd.append('file', file);
    setLoading(true);
    setUploadPct(0);
    try {
      const r = await AxiosInstance.post('/api/v1/documents/upload', fd, {
        headers: { 'Content-Type': 'multipart/form-data' },
        onUploadProgress: e => setUploadPct(e.total ? Math.round(e.loaded*100/e.total) : 50),
      });
      toast.success('Document uploaded successfully');
      setFile(null);
      setUploadPct(0);
      fetchDocuments();

      // Start polling for status
      const docId = r.data.data.document_id;
      pollDocumentStatus(docId);
    } catch(e) {
      toast.error(e.response?.data?.detail || 'Upload failed');
    } finally {
      setLoading(false);
    }
  };

  const pollDocumentStatus = (docId) => {
    const interval = setInterval(async () => {
      const status = await checkDocumentStatus(docId);
      if (status && (status.status === 'ready' || status.status === 'error')) {
        clearInterval(interval);
        fetchDocuments();
      }
    }, 3000);
  };

  const deleteDocument = async (docId, filename) => {
    if (!confirm(`Delete "${filename}"?`)) return;
    try {
      await AxiosInstance.delete(`/api/v1/documents/${docId}`);
      toast.success('Document deleted');
      fetchDocuments();
    } catch(e) {
      toast.error('Delete failed');
    }
  };

  const submitChat = async () => {
    if (!queryText.trim()) { toast.warn('Enter a question first'); return; }
    if (!selectedDoc) { toast.warn('Select a document first'); return; }

    setLoading(true);
    setChatResult(null);
    try {
      const endpoint = chatMode === 'agent' ? '/api/v1/chat/agent' : 
                      chatMode === 'simple' ? '/api/v1/chat/simple' : '/api/v1/chat';

      const r = await AxiosInstance.post(endpoint, {
        document_id: selectedDoc,
        question: queryText,
        top_k: topK,
      });

      setChatResult(r.data.data);
      setChatHistory(prev => [...prev, {
        question: queryText,
        answer: r.data.data,
        timestamp: new Date().toISOString()
      }]);
      toast.success('Query completed');
    } catch(e) {
      toast.error(e.response?.data?.detail || 'Query failed');
    } finally {
      setLoading(false);
    }
  };

  const submitSearch = async () => {
    if (!searchQuery.trim()) { toast.warn('Enter a search query first'); return; }
    if (!selectedDoc) { toast.warn('Select a document first'); return; }

    setLoading(true);
    try {
      const r = await AxiosInstance.post('/api/v1/search', {
        query: searchQuery,
        document_id: selectedDoc,
        top_k: topK,
      });
      setSearchResults(r.data.data.results || []);
      toast.success(`Found ${r.data.data.count} results`);
    } catch(e) {
      toast.error(e.response?.data?.detail || 'Search failed');
    } finally {
      setLoading(false);
    }
  };

  const submitExtraction = async () => {
    if (!extractionFields.trim()) { toast.warn('Enter fields to extract first'); return; }
    if (!selectedDoc) { toast.warn('Select a document first'); return; }

    const fields = extractionFields.split(',').map(f => f.trim()).filter(f => f);
    if (fields.length === 0) { toast.warn('Enter at least one field'); return; }

    setLoading(true);
    try {
      const r = await AxiosInstance.post(`/api/v1/extraction/${selectedDoc}`, {
        fields: fields,
      });
      setExtractionResult(r.data.data);
      toast.success('Extraction completed');
    } catch(e) {
      toast.error(e.response?.data?.detail || 'Extraction failed');
    } finally {
      setLoading(false);
    }
  };

  const generateSummary = async () => {
    if (!selectedDoc) { toast.warn('Select a document first'); return; }

    setLoading(true);
    try {
      const r = await AxiosInstance.post(`/api/v1/documents/${selectedDoc}/summary`);
      setSummaryResult(r.data.data);
      toast.success('Summary generated');
    } catch(e) {
      toast.error(e.response?.data?.detail || 'Summary generation failed');
    } finally {
      setLoading(false);
    }
  };

  const downloadReport = async () => {
    if (!selectedDoc) { toast.warn('Select a document first'); return; }

    try {
      const r = await AxiosInstance.get(`/api/v1/documents/${selectedDoc}/report`, {
        responseType: 'blob',
      });
      const url = window.URL.createObjectURL(new Blob([r.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `report_${selectedDoc}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      toast.success('Report downloaded');
    } catch(e) {
      toast.error('Report download failed');
    }
  };

  /* ─── Drag-drop ─── */
  const onDrop = useCallback(e => {
    e.preventDefault();
    setDragging(false);
    const f = e.dataTransfer.files[0];
    if (f && f.type === 'application/pdf') {
      setFile(f);
    } else {
      toast.warn('Please upload a PDF file');
    }
  }, []);

  const onDragOver = useCallback(e => {
    e.preventDefault();
    setDragging(true);
  }, []);

  const onDragLeave = useCallback(e => {
    e.preventDefault();
    setDragging(false);
  }, []);

  /* ─── TABS ─── */
  const TABS = [
    { id:'documents', label:'Documents' },
    { id:'chat',      label:'Chat' },
    { id:'search',    label:'Search' },
    { id:'extraction', label:'Extraction' },
    { id:'summary',   label:'Summary' },
  ];

  return (
    <>
      {mounted && <style suppressHydrationWarning>{GLOBAL_CSS}</style>}
      <Toasts />

      <div className="font-sans" style={{ background:'var(--charcoal)', minHeight:'100vh', color:'var(--text-primary)', position:'relative', zIndex:1 }}>

        {/* ═══ HEADER ═══ */}
        <header style={{ background:'rgba(13,13,13,0.95)', backdropFilter:'blur(20px)', borderBottom:'1px solid var(--border)', position:'sticky', top:0, zIndex:40 }}>
          <div style={{ maxWidth:1400, margin:'0 auto', padding:'0 32px', height:72, display:'flex', alignItems:'center', justifyContent:'space-between' }}>
            <div style={{ display:'flex', alignItems:'center', gap:24 }}>
              <div style={{ width:40, height:40, background:'linear-gradient(135deg, var(--gold), var(--gold-dark))', display:'flex', alignItems:'center', justifyContent:'center' }}>
                <span className="font-serif" style={{ fontSize:'1.4rem', color:'var(--charcoal)', fontWeight:700 }}>AI</span>
              </div>
              <div>
                <div className="font-serif" style={{ fontSize:'1.4rem', letterSpacing:'0.02em', lineHeight:1.2 }}>
                  <span className="gold-text">Document Processing</span>
                </div>
                <div className="font-mono" style={{ fontSize:'0.6rem', letterSpacing:'0.2em', color:'var(--text-muted)', textTransform:'uppercase', marginTop:4 }}>
                  RAG · Extraction · Search · Summary
                </div>
              </div>
            </div>
            <div style={{ display:'flex', alignItems:'center', gap:24 }}>
              <div style={{ display:'flex', alignItems:'center', gap:10 }}>
                <span style={{ width:6, height:6, borderRadius:'50%', background:'#10b981', boxShadow:'0 0 8px #10b981', display:'inline-block' }} />
                <span className="font-mono" style={{ fontSize:'0.65rem', letterSpacing:'0.1em', textTransform:'uppercase', color:'var(--text-secondary)' }}>
                  {documents.length} Documents
                </span>
              </div>
            </div>
          </div>
        </header>

        {/* ═══ TABS ═══ */}
        <div style={{ background:'var(--dark-charcoal)', borderBottom:'1px solid var(--border)', overflowX:'auto' }}>
          <div style={{ maxWidth:1400, margin:'0 auto', padding:'0 32px', display:'flex' }}>
            {TABS.map(t => (
              <button key={t.id} className={`tab-btn ${tab===t.id?'active':''}`}
                onClick={() => setTab(t.id)}>
                {t.label}
              </button>
            ))}
          </div>
        </div>

        {/* ═══ CONTENT ═══ */}
        <main style={{ maxWidth:1400, margin:'0 auto', padding:'32px 32px 60px' }}>

          {/* ── DOCUMENTS TAB ── */}
          {tab==='documents' && (
            <div style={{ display:'grid', gridTemplateColumns:'1fr 2fr', gap:24, alignItems:'start' }}>

              {/* Upload Panel */}
              <div style={{ display:'flex', flexDirection:'column', gap:20 }}>
                <Card>
                  <SectLabel>Upload Document</SectLabel>
                  <div
                    onDrop={onDrop}
                    onDragOver={onDragOver}
                    onDragLeave={onDragLeave}
                    style={{
                      border: `2px dashed ${dragging ? 'var(--gold)' : 'var(--border)'}`,
                      borderRadius: 8,
                      padding: 40,
                      textAlign: 'center',
                      cursor: 'pointer',
                      background: dragging ? 'rgba(212,175,55,0.05)' : 'var(--surface-2)',
                      transition: 'all 0.2s'
                    }}
                    onClick={() => fileRef.current?.click()}
                  >
                    <input
                      ref={fileRef}
                      type="file"
                      accept=".pdf"
                      style={{ display: 'none' }}
                      onChange={e => {
                        const f = e.target.files[0];
                        if (f && f.type === 'application/pdf') {
                          setFile(f);
                        } else {
                          toast.warn('Please upload a PDF file');
                        }
                      }}
                    />
                    <div style={{ fontSize: '2rem', marginBottom: 12 }}>📄</div>
                    <div style={{ color: 'var(--text-secondary)', marginBottom: 8 }}>
                      {file ? file.name : 'Drag & drop PDF here or click to browse'}
                    </div>
                    <div className="font-mono" style={{ fontSize: '0.65rem', color: 'var(--text-muted)' }}>
                      PDF files only, max 10MB
                    </div>
                  </div>

                  {file && (
                    <div style={{ marginTop: 16 }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                        <span className="font-mono" style={{ fontSize: '0.7rem', color: 'var(--text-secondary)' }}>
                          {file.name}
                        </span>
                        <span className="font-mono" style={{ fontSize: '0.7rem', color: 'var(--gold)' }}>
                          {fmt.bytes(file.size)}
                        </span>
                      </div>
                      {uploadPct > 0 && (
                        <div className="prog-bar" style={{ marginBottom: 12 }}>
                          <div className="prog-fill" style={{ width: `${uploadPct}%` }} />
                        </div>
                      )}
                      <div style={{ display: 'flex', gap: 12 }}>
                        <WhiteBtn loading={loading} loadText="Uploading…" onClick={uploadDocument} disabled={loading} style={{ flex: 1 }}>
                          Upload
                        </WhiteBtn>
                        <button className="btn-ghost" onClick={() => { setFile(null); setUploadPct(0); }}>
                          Clear
                        </button>
                      </div>
                    </div>
                  )}
                </Card>

                <Card>
                  <SectLabel>Document Stats</SectLabel>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
                    <div>
                      <div className="font-mono" style={{ fontSize: '0.65rem', color: 'var(--text-muted)', marginBottom: 4 }}>Total Documents</div>
                      <div className="font-serif" style={{ fontSize: '1.8rem', color: 'var(--gold)' }}>{documents.length}</div>
                    </div>
                    <div>
                      <div className="font-mono" style={{ fontSize: '0.65rem', color: 'var(--text-muted)', marginBottom: 4 }}>Ready</div>
                      <div className="font-serif" style={{ fontSize: '1.8rem', color: 'var(--emerald)' }}>
                        {documents.filter(d => d.status === 'ready').length}
                      </div>
                    </div>
                  </div>
                </Card>
              </div>

              {/* Documents List */}
              <Card>
                <SectLabel>Document Library</SectLabel>
                {documents.length === 0 ? (
                  <div style={{ textAlign: 'center', padding: 40, color: 'var(--text-muted)' }}>
                    <div style={{ fontSize: '2rem', marginBottom: 12 }}>📭</div>
                    <div>No documents uploaded yet</div>
                  </div>
                ) : (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
                    {documents.map(doc => (
                      <div
                        key={doc.id}
                        onClick={() => setSelectedDoc(doc.id)}
                        style={{
                          background: selectedDoc === doc.id ? 'rgba(212,175,55,0.1)' : 'var(--surface-2)',
                          border: `1px solid ${selectedDoc === doc.id ? 'var(--gold)' : 'var(--border)'}`,
                          borderRadius: 8,
                          padding: 16,
                          cursor: 'pointer',
                          transition: 'all 0.2s'
                        }}
                      >
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: 8 }}>
                          <div style={{ flex: 1 }}>
                            <div style={{ fontWeight: 600, marginBottom: 4 }}>{doc.filename}</div>
                            <div className="font-mono" style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>
                              {fmt.bytes(doc.file_size_mb * 1024 * 1024)} • {doc.page_count || '?'} pages
                            </div>
                          </div>
                          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                            <HDot status={doc.status} />
                            <Badge color={doc.status === 'ready' ? '#10b981' : doc.status === 'processing' ? '#f59e0b' : '#ef4444'}>
                              {doc.status}
                            </Badge>
                          </div>
                        </div>
                        {doc.progress && doc.progress < 100 && (
                          <div className="prog-bar" style={{ marginTop: 8 }}>
                            <div className="prog-fill" style={{ width: `${doc.progress}%` }} />
                          </div>
                        )}
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: 12 }}>
                          <div className="font-mono" style={{ fontSize: '0.65rem', color: 'var(--text-muted)' }}>
                            {fmt.date(doc.created_at)}
                          </div>
                          <button
                            className="btn-danger"
                            onClick={(e) => { e.stopPropagation(); deleteDocument(doc.id, doc.filename); }}
                            style={{ padding: '6px 12px', fontSize: '0.65rem' }}
                          >
                            Delete
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </Card>
            </div>
          )}

          {/* ── CHAT TAB ── */}
          {tab==='chat' && (
            <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:24, alignItems:'start' }}>

              {/* Chat Input */}
              <div style={{ display:'flex', flexDirection:'column', gap:20 }}>
                <Card>
                  <SectLabel>Document Selection</SectLabel>
                  <select
                    className="inp"
                    value={selectedDoc || ''}
                    onChange={e => setSelectedDoc(e.target.value)}
                    style={{ marginBottom: 20 }}
                  >
                    <option value="">Select a document...</option>
                    {documents.filter(d => d.status === 'ready').map(d => (
                      <option key={d.id} value={d.id}>{d.filename}</option>
                    ))}
                  </select>

                  <SectLabel>Chat Mode</SectLabel>
                  <select
                    className="inp"
                    value={chatMode}
                    onChange={e => setChatMode(e.target.value)}
                    style={{ marginBottom: 20 }}
                  >
                    <option value="auto">Auto (System decides)</option>
                    <option value="agent">CRAG Agent (Advanced)</option>
                    <option value="simple">Simple RAG (Fast)</option>
                  </select>

                  <SectLabel>Your Question</SectLabel>
                  <textarea
                    className="inp"
                    rows={5}
                    value={queryText}
                    onChange={e => setQueryText(e.target.value)}
                    placeholder="Ask anything about your document..."
                    style={{ marginBottom: 16, resize: 'vertical', lineHeight: 1.6 }}
                  />

                  <div style={{ marginBottom: 16 }}>
                    <label className="font-mono" style={{ fontSize: '0.7rem', letterSpacing: '0.12em', textTransform: 'uppercase', color: 'var(--gold)', display: 'block', marginBottom: 8, fontWeight: 600 }}>
                      Top-K Chunks
                    </label>
                    <input
                      className="inp"
                      type="number"
                      min={1}
                      max={20}
                      value={topK}
                      onChange={e => setTopK(+e.target.value)}
                    />
                  </div>

                  <WhiteBtn loading={loading} loadText="Processing…" onClick={submitChat} disabled={loading || !selectedDoc} style={{ width: '100%' }}>
                    Ask Question
                  </WhiteBtn>
                </Card>

                {chatHistory.length > 0 && (
                  <Card>
                    <SectLabel>Chat History</SectLabel>
                    <div style={{ maxHeight: 300, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: 12 }}>
                      {chatHistory.slice().reverse().map((item, i) => (
                        <div key={i} style={{ borderBottom: '1px solid var(--border)', paddingBottom: 12 }}>
                          <div className="font-mono" style={{ fontSize: '0.7rem', color: 'var(--gold)', marginBottom: 4 }}>
                            Q: {item.question}
                          </div>
                          <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: 4 }}>
                            {item.answer?.answer?.substring(0, 100)}...
                          </div>
                          <div className="font-mono" style={{ fontSize: '0.65rem', color: 'var(--text-muted)' }}>
                            {fmt.date(item.timestamp)}
                          </div>
                        </div>
                      ))}
                    </div>
                  </Card>
                )}
              </div>

              {/* Chat Result */}
              <div style={{ display:'flex', flexDirection:'column', gap:20 }}>
                {chatResult ? (
                  <Card>
                    <SectLabel>Answer</SectLabel>
                    <div style={{ display:'flex', flexWrap:'wrap', gap:8, marginBottom:16 }}>
                      <Badge color="#d4af37">{chatResult.mode}</Badge>
                      <Badge color="#3b82f6">{chatResult.chunks_used} chunks</Badge>
                      {chatResult.iterations && <Badge color="#10b981">{chatResult.iterations} iterations</Badge>}
                      {chatResult.query_rewritten && <Badge color="#f59e0b">Query rewritten</Badge>}
                    </div>

                    <div style={{ background:'var(--surface-2)', borderLeft:'3px solid var(--gold)', padding:'20px 24px', fontSize:'0.95rem', color:'var(--text-primary)', lineHeight:1.7, whiteSpace:'pre-wrap', marginBottom:20 }}>
                      {chatResult.answer}
                    </div>

                    {chatResult.citations && chatResult.citations.length > 0 && (
                      <div>
                        <div className="font-mono" style={{ fontSize:'0.65rem', letterSpacing:'0.15em', textTransform:'uppercase', color:'var(--text-muted)', marginBottom:12, fontWeight:600 }}>
                          Citations
                        </div>
                        <div style={{ display:'flex', flexDirection:'column', gap: 8 }}>
                          {chatResult.citations.map((citation, i) => (
                            <div key={i} style={{ background:'var(--surface-2)', padding: 12, borderRadius: 4, fontSize: '0.8rem' }}>
                              <div className="font-mono" style={{ fontSize: '0.65rem', color: 'var(--gold)', marginBottom: 4 }}>
                                Page {citation.page_number}
                              </div>
                              <div style={{ color: 'var(--text-secondary)' }}>
                                {fmt.cut(citation.content, 150)}
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </Card>
                ) : (
                  <Card>
                    <div style={{ textAlign: 'center', padding: 40, color: 'var(--text-muted)' }}>
                      <div style={{ fontSize: '2rem', marginBottom: 12 }}>💬</div>
                      <div>Select a document and ask a question</div>
                    </div>
                  </Card>
                )}
              </div>
            </div>
          )}

          {/* ── SEARCH TAB ── */}
          {tab==='search' && (
            <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:24, alignItems:'start' }}>

              {/* Search Input */}
              <div style={{ display:'flex', flexDirection:'column', gap:20 }}>
                <Card>
                  <SectLabel>Document Selection</SectLabel>
                  <select
                    className="inp"
                    value={selectedDoc || ''}
                    onChange={e => setSelectedDoc(e.target.value)}
                    style={{ marginBottom: 20 }}
                  >
                    <option value="">Select a document...</option>
                    {documents.filter(d => d.status === 'ready').map(d => (
                      <option key={d.id} value={d.id}>{d.filename}</option>
                    ))}
                  </select>

                  <SectLabel>Search Query</SectLabel>
                  <textarea
                    className="inp"
                    rows={3}
                    value={searchQuery}
                    onChange={e => setSearchQuery(e.target.value)}
                    placeholder="Enter search terms..."
                    style={{ marginBottom: 16, resize: 'vertical' }}
                  />

                  <div style={{ marginBottom: 16 }}>
                    <label className="font-mono" style={{ fontSize: '0.7rem', letterSpacing: '0.12em', textTransform: 'uppercase', color: 'var(--gold)', display: 'block', marginBottom: 8, fontWeight: 600 }}>
                      Top-K Results
                    </label>
                    <input
                      className="inp"
                      type="number"
                      min={1}
                      max={20}
                      value={topK}
                      onChange={e => setTopK(+e.target.value)}
                    />
                  </div>

                  <WhiteBtn loading={loading} loadText="Searching…" onClick={submitSearch} disabled={loading || !selectedDoc} style={{ width: '100%' }}>
                    Search Document
                  </WhiteBtn>
                </Card>
              </div>

              {/* Search Results */}
              <div style={{ display:'flex', flexDirection:'column', gap:20 }}>
                {searchResults.length > 0 ? (
                  <Card>
                    <SectLabel>Search Results ({searchResults.length})</SectLabel>
                    <div style={{ display:'flex', flexDirection:'column', gap: 12 }}>
                      {searchResults.map((result, i) => (
                        <div key={i} style={{ background:'var(--surface-2)', padding: 16, borderRadius: 8, border: '1px solid var(--border)' }}>
                          <div style={{ display:'flex', justifyContent:'space-between', marginBottom: 8 }}>
                            <Badge color="#3b82f6">Page {result.page_number}</Badge>
                            <Badge color="#d4af37">{(result.similarity * 100).toFixed(1)}% similar</Badge>
                          </div>
                          <div style={{ fontSize: '0.9rem', color: 'var(--text-primary)', lineHeight: 1.6 }}>
                            {result.content}
                          </div>
                        </div>
                      ))}
                    </div>
                  </Card>
                ) : (
                  <Card>
                    <div style={{ textAlign: 'center', padding: 40, color: 'var(--text-muted)' }}>
                      <div style={{ fontSize: '2rem', marginBottom: 12 }}>🔍</div>
                      <div>Search results will appear here</div>
                    </div>
                  </Card>
                )}
              </div>
            </div>
          )}

          {/* ── EXTRACTION TAB ── */}
          {tab==='extraction' && (
            <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:24, alignItems:'start' }}>

              {/* Extraction Input */}
              <div style={{ display:'flex', flexDirection:'column', gap:20 }}>
                <Card>
                  <SectLabel>Document Selection</SectLabel>
                  <select
                    className="inp"
                    value={selectedDoc || ''}
                    onChange={e => setSelectedDoc(e.target.value)}
                    style={{ marginBottom: 20 }}
                  >
                    <option value="">Select a document...</option>
                    {documents.filter(d => d.status === 'ready').map(d => (
                      <option key={d.id} value={d.id}>{d.filename}</option>
                    ))}
                  </select>

                  <SectLabel>Fields to Extract</SectLabel>
                  <textarea
                    className="inp"
                    rows={4}
                    value={extractionFields}
                    onChange={e => setExtractionFields(e.target.value)}
                    placeholder="Enter fields separated by commas (e.g., company_name, revenue, employees, founded_year)"
                    style={{ marginBottom: 16, resize: 'vertical' }}
                  />

                  <div className="font-mono" style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginBottom: 16 }}>
                    Maximum 20 fields per request
                  </div>

                  <WhiteBtn loading={loading} loadText="Extracting…" onClick={submitExtraction} disabled={loading || !selectedDoc} style={{ width: '100%' }}>
                    Extract Fields
                  </WhiteBtn>
                </Card>
              </div>

              {/* Extraction Results */}
              <div style={{ display:'flex', flexDirection:'column', gap:20 }}>
                {extractionResult ? (
                  <Card>
                    <SectLabel>Extraction Results</SectLabel>
                    <div style={{ marginBottom: 16 }}>
                      <div className="font-mono" style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginBottom: 8 }}>
                        Document: {extractionResult.filename}
                      </div>
                      <div className="font-mono" style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>
                        Model: {extractionResult.model}
                      </div>
                    </div>

                    <div style={{ display: 'grid', gap: 12 }}>
                      {Object.entries(extractionResult.fields).map(([field, data]) => (
                        <div key={field} style={{ background:'var(--surface-2)', padding: 16, borderRadius: 8, border: '1px solid var(--border)' }}>
                          <div className="font-mono" style={{ fontSize: '0.7rem', color: 'var(--gold)', marginBottom: 8, fontWeight: 600 }}>
                            {field}
                          </div>
                          <div style={{ fontSize: '0.9rem', color: 'var(--text-primary)', marginBottom: 4 }}>
                            {data.value || 'Not found'}
                          </div>
                          <Badge color={data.status === 'found' ? '#10b981' : data.status === 'not_found' ? '#ef4444' : '#f59e0b'}>
                            {data.status}
                          </Badge>
                        </div>
                      ))}
                    </div>
                  </Card>
                ) : (
                  <Card>
                    <div style={{ textAlign: 'center', padding: 40, color: 'var(--text-muted)' }}>
                      <div style={{ fontSize: '2rem', marginBottom: 12 }}>⚡</div>
                      <div>Extraction results will appear here</div>
                    </div>
                  </Card>
                )}
              </div>
            </div>
          )}

          {/* ── SUMMARY TAB ── */}
          {tab==='summary' && (
            <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:24, alignItems:'start' }}>

              {/* Summary Controls */}
              <div style={{ display:'flex', flexDirection:'column', gap:20 }}>
                <Card>
                  <SectLabel>Document Selection</SectLabel>
                  <select
                    className="inp"
                    value={selectedDoc || ''}
                    onChange={e => setSelectedDoc(e.target.value)}
                    style={{ marginBottom: 20 }}
                  >
                    <option value="">Select a document...</option>
                    {documents.filter(d => d.status === 'ready').map(d => (
                      <option key={d.id} value={d.id}>{d.filename}</option>
                    ))}
                  </select>

                  <div style={{ display: 'flex', gap: 12, marginBottom: 16 }}>
                    <WhiteBtn loading={loading} loadText="Generating…" onClick={generateSummary} disabled={loading || !selectedDoc} style={{ flex: 1 }}>
                      Generate Summary
                    </WhiteBtn>
                    <button
                      className="btn-ghost"
                      onClick={downloadReport}
                      disabled={!selectedDoc}
                      style={{ flex: 1 }}
                    >
                      Download Report
                    </button>
                  </div>

                  <div className="font-mono" style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>
                    Summary uses AI to analyze document content and extract key information
                  </div>
                </Card>

                {selectedDoc && (
                  <Card>
                    <SectLabel>Document Info</SectLabel>
                    {(() => {
                      const doc = documents.find(d => d.id === selectedDoc);
                      return doc ? (
                        <div style={{ display: 'grid', gap: 12 }}>
                          <div>
                            <div className="font-mono" style={{ fontSize: '0.65rem', color: 'var(--text-muted)', marginBottom: 4 }}>Filename</div>
                            <div>{doc.filename}</div>
                          </div>
                          <div>
                            <div className="font-mono" style={{ fontSize: '0.65rem', color: 'var(--text-muted)', marginBottom: 4 }}>Size</div>
                            <div>{fmt.bytes(doc.file_size_mb * 1024 * 1024)}</div>
                          </div>
                          <div>
                            <div className="font-mono" style={{ fontSize: '0.65rem', color: 'var(--text-muted)', marginBottom: 4 }}>Pages</div>
                            <div>{doc.page_count || 'Processing...'}</div>
                          </div>
                          <div>
                            <div className="font-mono" style={{ fontSize: '0.65rem', color: 'var(--text-muted)', marginBottom: 4 }}>Status</div>
                            <Badge color={doc.status === 'ready' ? '#10b981' : '#f59e0b'}>{doc.status}</Badge>
                          </div>
                        </div>
                      ) : null;
                    })()}
                  </Card>
                )}
              </div>

              {/* Summary Results */}
              <div style={{ display:'flex', flexDirection:'column', gap:20 }}>
                {summaryResult ? (
                  <Card>
                    <SectLabel>AI Summary</SectLabel>
                    <div style={{ marginBottom: 20 }}>
                      <div className="font-mono" style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginBottom: 8 }}>
                        Model: {summaryResult.model}
                      </div>
                    </div>

                    {summaryResult.executive_summary && (
                      <div style={{ marginBottom: 20 }}>
                        <div className="font-mono" style={{ fontSize: '0.7rem', color: 'var(--gold)', marginBottom: 8, fontWeight: 600 }}>
                          Executive Summary
                        </div>
                        <div style={{ background:'var(--surface-2)', padding: 16, borderRadius: 8, lineHeight: 1.6 }}>
                          {summaryResult.executive_summary}
                        </div>
                      </div>
                    )}

                    {summaryResult.key_points && summaryResult.key_points.length > 0 && (
                      <div style={{ marginBottom: 20 }}>
                        <div className="font-mono" style={{ fontSize: '0.7rem', color: 'var(--gold)', marginBottom: 8, fontWeight: 600 }}>
                          Key Points
                        </div>
                        <ul style={{ margin: 0, paddingLeft: 20 }}>
                          {summaryResult.key_points.map((point, i) => (
                            <li key={i} style={{ marginBottom: 8, lineHeight: 1.6 }}>{point}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {summaryResult.important_facts && summaryResult.important_facts.length > 0 && (
                      <div style={{ marginBottom: 20 }}>
                        <div className="font-mono" style={{ fontSize: '0.7rem', color: 'var(--gold)', marginBottom: 8, fontWeight: 600 }}>
                          Important Facts
                        </div>
                        <ul style={{ margin: 0, paddingLeft: 20 }}>
                          {summaryResult.important_facts.map((fact, i) => (
                            <li key={i} style={{ marginBottom: 8, lineHeight: 1.6 }}>{fact}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {summaryResult.important_numbers && summaryResult.important_numbers.length > 0 && (
                      <div style={{ marginBottom: 20 }}>
                        <div className="font-mono" style={{ fontSize: '0.7rem', color: 'var(--gold)', marginBottom: 8, fontWeight: 600 }}>
                          Important Numbers
                        </div>
                        <ul style={{ margin: 0, paddingLeft: 20 }}>
                          {summaryResult.important_numbers.map((num, i) => (
                            <li key={i} style={{ marginBottom: 8, lineHeight: 1.6 }}>{num}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {summaryResult.risks && summaryResult.risks.length > 0 && (
                      <div style={{ marginBottom: 20 }}>
                        <div className="font-mono" style={{ fontSize: '0.7rem', color: 'var(--ruby)', marginBottom: 8, fontWeight: 600 }}>
                          Risks
                        </div>
                        <ul style={{ margin: 0, paddingLeft: 20 }}>
                          {summaryResult.risks.map((risk, i) => (
                            <li key={i} style={{ marginBottom: 8, lineHeight: 1.6, color: 'var(--ruby)' }}>{risk}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {summaryResult.conclusion && (
                      <div>
                        <div className="font-mono" style={{ fontSize: '0.7rem', color: 'var(--gold)', marginBottom: 8, fontWeight: 600 }}>
                          Conclusion
                        </div>
                        <div style={{ background:'var(--surface-2)', padding: 16, borderRadius: 8, lineHeight: 1.6 }}>
                          {summaryResult.conclusion}
                        </div>
                      </div>
                    )}
                  </Card>
                ) : (
                  <Card>
                    <div style={{ textAlign: 'center', padding: 40, color: 'var(--text-muted)' }}>
                      <div style={{ fontSize: '2rem', marginBottom: 12 }}>📋</div>
                      <div>Select a document and generate summary</div>
                    </div>
                  </Card>
                )}
              </div>
            </div>
          )}

        </main>
      </div>
    </>
  );
}