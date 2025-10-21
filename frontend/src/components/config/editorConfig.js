// editorConfig.js

// Mappa estensioni file a linguaggi Monaco Editor
export const getLanguageFromExtension = (extension) => {
    const languageMap = {
    // C/C++ family
    '.c': 'c',
    '.cpp': 'cpp',
    '.cc': 'cpp',
    '.cxx': 'cpp',
    '.cu': 'cpp', // CUDA uses C++ syntax
    '.cuh': 'cpp', // CUDA header files
    
    // Web technologies
    '.js': 'javascript',
    '.ts': 'typescript',
    '.html': 'html',
    '.css': 'css',
    '.scss': 'scss',
    '.less': 'less',
    '.json': 'json',
    '.xml': 'xml',
    
    // Programming languages
    '.py': 'python',
    '.java': 'java',
    '.cs': 'csharp',
    '.php': 'php',
    '.rb': 'ruby',
    '.go': 'go',
    '.rs': 'rust',
    '.swift': 'swift',
    '.kt': 'kotlin',
    '.r': 'r',
    '.sql': 'sql',
    
    // Markup and config
    '.md': 'markdown',
    '.yaml': 'yaml',
    '.yml': 'yaml',
    
    // Shell scripts
    '.sh': 'shell',
    '.bash': 'shell',
    '.ps1': 'powershell',
    
    // Build and config files
    '.dockerfile': 'dockerfile',
    '.makefile': 'makefile',
    '.ini': 'ini',
    '.properties': 'properties',
    
    // Fallback for unsupported languages
    '.txt': 'plaintext',
    '.log': 'plaintext',
    '.plain': 'plaintext'
    };
    
    return languageMap[extension?.toLowerCase()] || 'c';
};

// Mappa estensioni file a nomi linguaggi per UI
export const getLanguageNameFromExtension = (extension) => {
    const nameMap = {
    // C/C++ family
    '.c': 'C',
    '.cpp': 'C++',
    '.cc': 'C++',
    '.cxx': 'C++',
    '.cu': 'CUDA C++',
    '.cuh': 'CUDA C++',
    
    // Web technologies
    '.js': 'JavaScript',
    '.ts': 'TypeScript',
    '.html': 'HTML',
    '.css': 'CSS',
    '.scss': 'SCSS',
    '.less': 'Less',
    '.json': 'JSON',
    '.xml': 'XML',
    
    // Programming languages
    '.py': 'Python',
    '.java': 'Java',
    '.cs': 'C#',
    '.php': 'PHP',
    '.rb': 'Ruby',
    '.go': 'Go',
    '.rs': 'Rust',
    '.swift': 'Swift',
    '.kt': 'Kotlin',
    '.r': 'R',
    '.sql': 'SQL',
    
    // Markup and config
    '.md': 'Markdown',
    '.yaml': 'YAML',
    '.yml': 'YAML',
    
    // Shell scripts
    '.sh': 'Shell',
    '.bash': 'Bash',
    '.ps1': 'PowerShell',
    
    // Build and config files
    '.dockerfile': 'Dockerfile',
    '.makefile': 'Makefile',
    '.ini': 'INI',
    '.properties': 'Properties',
    
    // Fallback
    '.txt': 'Plain Text',
    '.log': 'Log',
    '.plain': 'Plain Text'
    };
    
    return nameMap[extension?.toLowerCase()] || 'C';
};

// Mappa estensioni file a compilatori per UI
export const getCompilerFromExtension = (extension) => {
    const compilerMap = {
    // C/C++ family
    '.c': 'GCC',
    '.cpp': 'G++',
    '.cc': 'G++',
    '.cxx': 'G++',
    '.cu': 'NVCC',
    '.cuh': 'NVCC',
    
    // Web technologies
    '.js': 'Node.js',
    '.ts': 'TypeScript',
    '.html': 'Browser',
    '.css': 'Browser',
    '.scss': 'Sass',
    '.less': 'Less',
    '.json': 'JSON',
    '.xml': 'XML',
    
    // Programming languages
    '.py': 'Python',
    '.java': 'javac',
    '.cs': 'csc',
    '.php': 'PHP',
    '.rb': 'Ruby',
    '.go': 'go',
    '.rs': 'rustc',
    '.swift': 'swiftc',
    '.kt': 'kotlinc',
    '.r': 'R',
    '.sql': 'SQL',
    
    // Markup and config
    '.md': 'Markdown',
    '.yaml': 'YAML',
    '.yml': 'YAML',
    
    // Shell scripts
    '.sh': 'Bash',
    '.bash': 'Bash',
    '.ps1': 'PowerShell',
    
    // Build and config files
    '.dockerfile': 'Docker',
    '.makefile': 'Make',
    '.ini': 'Config',
    '.properties': 'Properties',
    
    // Fallback
    '.txt': 'Text',
    '.log': 'Log',
    '.plain': 'Text'
    };
    
    return compilerMap[extension?.toLowerCase()] || 'GCC';
};

// Configurazione opzioni editor
export const getEditorOptions = (language) => {
    const baseOptions = {
    fontSize: 14,
    minimap: { enabled: false },
    automaticLayout: true,
    lineNumbers: 'on',
    wordWrap: 'on',
    scrollBeyondLastLine: false,
    padding: { top: 16, bottom: 16 },
    fontFamily: "'Fira Code', 'Consolas', 'Monaco', monospace",
    fontLigatures: true,
    };

    // Opzioni specifiche per linguaggio
    const languageSpecificOptions = {
    cpp: {
        quickSuggestions: true,
        parameterHints: { enabled: true },
    },
    c: {
        quickSuggestions: true,
        parameterHints: { enabled: true },
    },
    python: {
        quickSuggestions: true,
    },
    javascript: {
        quickSuggestions: true,
        suggest: { 
        showKeywords: true,
        showSnippets: true 
        },
    },
    // Aggiungi altre configurazioni specifiche qui
    };

    return {
    ...baseOptions,
    ...(languageSpecificOptions[language] || {})
    };
};

// Supporto CUDA - Configurazione semplificata
export const configureCUDASupport = (monaco) => {
    // Solo se Monaco è disponibile
    if (!monaco) return;

    try {
    // Registra linguaggio CUDA personalizzato (opzionale)
    monaco.languages.register({ id: 'cuda-cpp' });
    
    console.log('Supporto CUDA configurato per Monaco Editor');
    } catch (error) {
    console.warn('Errore nella configurazione CUDA:', error);
    }
};

// Esporta tutte le configurazioni
export default {
    getLanguageFromExtension,
    getLanguageNameFromExtension,
    getCompilerFromExtension,
    getEditorOptions,
    configureCUDASupport
};