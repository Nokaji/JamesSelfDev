import { Hono } from 'hono';
import { isRunningOnBun } from './utils/runtime';
import Logging from './utils/logging';

const { serveStatic } = isRunningOnBun()
  ? await import("hono/bun")
  : await import("@hono/node-server/serve-static");
const { serve } = isRunningOnBun()
  ? await import("bun")
  : await import("@hono/node-server");

class App {
  app: Hono = new Hono();
  startTime: number = Date.now();
  logger: Logging = Logging.getInstance();

  constructor() {
    this.initRoutes();
    this.initServer();
  };

  private async initRoutes() {

  }

  private async initServer() {
    // const port = ConfigManager.APP.PORT;
    // const host = ConfigManager.APP.HOST;

    serve(
      {
        fetch: this.app.fetch,
        port,
        // ...(ConfigManager.isProduction() && host !== "0.0.0.0" ? { hostname: host } : {})
      },
      (info) => {
        if (info) {
          this.logger.error('Server startup error:', info);
          // if (ConfigManager.isProduction()) {
          //   process.exit(1);
          // }
        }
      }
    );

    const startupTime = Date.now() - this.startTime;
    this.logger.info(`🚀 Server started in ${startupTime}ms`);
    // this.logger.info(`🌐 Listening at http://${host}:${port}`);
    // this.logger.info(`📦 Environment: ${ConfigManager.APP.ENV}`);
    // if (this.dbManager.getDatabaseNames().length > 0)
    //   this.logger.info(`🗄️  Databases: ${this.dbManager.getDatabaseNames().join(', ')}`);

    // Graceful shutdown
    const gracefulShutdown = async (signal: string) => {
      this.logger.info(`Received ${signal}, starting graceful shutdown...`);
      try {
        // await this.dbManager.disconnectAll();
        this.logger.info('Graceful shutdown completed successfully');
        process.exit(0);
      } catch (error: any) {
        // En cas d'erreur lors de la fermeture, on log mais on continue l'arrêt
        this.logger.warn('Warning during shutdown (non-critical):', error?.message || error);
        this.logger.info('Shutdown completed with warnings');
        process.exit(0); // Sortie normale malgré les avertissements
      }
    };

    process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
    process.on('SIGINT', () => gracefulShutdown('SIGINT'));
  }
}