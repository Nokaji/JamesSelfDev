import path from 'path';
import fs from 'fs';

class ConfigManager {

    private instance: ConfigManager | null = null;
    public path: string;

    private constructor() {
        const home = process.env.HOME || process.env.USERPROFILE;
        if (!home) throw new Error('Cannot determine user home directory.');
        this.path = process.platform === 'darwin'
            ? path.join(home, 'Library', 'Application Support')
            : path.join(home, '.config');

        this.path = path.join(this.path, 'James', 'services', 'JamesSelfDev');
        if (!fs.existsSync(this.path)) fs.mkdirSync(this.path, { recursive: true });
        this.loadConfig();
    }

    public async getInstance() {
        if (!this.instance)
            this.instance = new ConfigManager();
        return this.instance;
    }

    private loadConfig() {

    }
};